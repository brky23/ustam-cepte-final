from django.shortcuts import render, redirect, get_object_or_404
from .models import Dukkan, Yorum, Arac, Favori
from django.db.models import Q
from datetime import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import KayitFormu, DukkanForm, AracForm
from django.contrib import messages

# 1. ANASAYFA (Garaj Arabası ve Arama Dahil)
def home(request):
    secilen_kategori = request.GET.get('kategori')
    arama_terimi = request.GET.get('q') 
    
    # Sadece YAYINDA olanları getir (Onaylanmamışlar gizli kalsın)
    dukkanlar = Dukkan.objects.filter(yayinda=True).order_by('-vitrin_uye', '-onayli_esnaf')

    if secilen_kategori and secilen_kategori != 'TUMU':
        dukkanlar = dukkanlar.filter(kategori=secilen_kategori)

    if arama_terimi:
        dukkanlar = dukkanlar.filter(
            Q(isim__icontains=arama_terimi) | 
            Q(uzmanlik__icontains=arama_terimi) | 
            Q(adres__icontains=arama_terimi)
        )

    # GARAJ: Kullanıcının arabası varsa getir (Anasayfadaki AI Hesaplayıcıya otomatik doldurmak için)
    kullanici_araci = None
    if request.user.is_authenticated:
        try:
            kullanici_araci = Arac.objects.get(kullanici=request.user)
        except Arac.DoesNotExist:
            kullanici_araci = None

    context = {
        'dukkanlar': dukkanlar,
        'secilen_kategori': secilen_kategori,
        'arama_terimi': arama_terimi,
        'kullanici_araci': kullanici_araci
    }
    return render(request, 'home.html', context)


# 2. DÜKKAN DETAY (7/24, İstatistik, Yorum, Favori, Sayaç Hepsi Var)
def dukkan_detay(request, id):
    dukkan = get_object_or_404(Dukkan, id=id)
    
    # Görüntülenme Sayacını Artır (Gerçek Sayaç)
    dukkan.goruntulenme += 1
    dukkan.save()

    # Açık/Kapalı Kontrolü (7/24 Mantığı Eklendi)
    saat = datetime.now().hour
    if dukkan.nobetci:
        acik_mi = True # Nöbetçiyse saate bakma, hep açık
    else:
        acik_mi = 8 <= saat < 19 # Değilse mesai saati

    # Favori Kontrolü
    favori_var_mi = False
    if request.user.is_authenticated:
        favori_var_mi = Favori.objects.filter(kullanici=request.user, dukkan=dukkan).exists()

    # ESNAFI HEYECANLANDIRAN SAHTE İSTATİSTİK FORMÜLÜ
    # (ID * 17) % 200 -> Her dükkana özel sabit rastgele sayı.
    haftalik_goruntulenme = ((dukkan.id * 17) % 200) + 45 + dukkan.goruntulenme
    aranma_sayisi = ((dukkan.id * 5) % 20) + 3

    # Yorum Kaydetme İşlemi
    if request.method == "POST" and request.user.is_authenticated:
        try:
            puan = request.POST.get('puan')
            metin = request.POST.get('metin')
            
            if puan and metin:
                Yorum.objects.create(
                    dukkan=dukkan,
                    kullanici=request.user,
                    puan=puan,
                    metin=metin
                )
                messages.success(request, "Yorumunuz başarıyla eklendi!")
                return redirect('dukkan_detay', id=id)
        except Exception as e:
            messages.error(request, "Hata oluştu.")

    # Yorumları Getir ve Puan Hesapla
    yorumlar = dukkan.yorumlar.all()
    if yorumlar:
        toplam = sum([y.puan for y in yorumlar])
        ortalama = round(toplam / len(yorumlar), 1)
    else:
        ortalama = 0

    context = {
        'dukkan': dukkan,
        'acik_mi': acik_mi,
        'yorumlar': yorumlar,
        'ortalama': ortalama,
        'favori_var_mi': favori_var_mi,
        'haftalik_goruntulenme': haftalik_goruntulenme, 
        'aranma_sayisi': aranma_sayisi 
    }
    
    return render(request, 'dukkan_detay.html', context)


# 3. KAYIT OL (E-Posta Destekli)
def kayit_ol(request):
    if request.method == "POST":
        form = KayitFormu(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Kaydınız başarıyla oluşturuldu!")
            return redirect('home')
    else:
        form = KayitFormu()
    return render(request, 'kayit_ol.html', {'form': form})


# 4. GİRİŞ YAP
def giris_yap(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Kullanıcı adı veya şifre hatalı.")
        else:
            messages.error(request, "Bilgileri kontrol edin.")
    form = AuthenticationForm()
    return render(request, 'giris_yap.html', {'form': form})


# 5. ÇIKIŞ YAP
def cikis_yap(request):
    logout(request)
    return redirect('home')


# 6. ESNAF KAYIT (Onay Bekleyen Sistem)
def esnaf_kayit(request):
    if request.method == "POST":
        form = DukkanForm(request.POST, request.FILES)
        if form.is_valid():
            dukkan = form.save(commit=False)
            # Yeni kayıtlar GİZLİ başlasın, sen onaylayınca görünsün
            dukkan.onayli_esnaf = False 
            dukkan.vitrin_uye = False
            dukkan.yayinda = False  
            dukkan.save()
            messages.success(request, "Başvurunuz alındı! Onay bekliyor.")
            return redirect('home')
    else:
        form = DukkanForm()
    return render(request, 'esnaf_kayit.html', {'form': form})


# 7. PROFİLİM / GARAJIM
def profil(request):
    if not request.user.is_authenticated:
        return redirect('giris_yap')
    
    try:
        arac = request.user.arac
    except Arac.DoesNotExist:
        arac = None

    # Kullanıcının favorilerini getir
    favoriler = Favori.objects.filter(kullanici=request.user).order_by('-tarih')

    if request.method == 'POST':
        form = AracForm(request.POST, instance=arac)
        if form.is_valid():
            yeni_arac = form.save(commit=False)
            yeni_arac.kullanici = request.user
            yeni_arac.save()
            messages.success(request, "Garaj bilgileriniz güncellendi!")
            return redirect('profil')
    else:
        form = AracForm(instance=arac)

    return render(request, 'profil.html', {'form': form, 'arac': arac, 'favoriler': favoriler})


# 8. FAVORİ İŞLEM (Ekle/Çıkar)
def favori_islem(request, id):
    if not request.user.is_authenticated:
        messages.warning(request, "Favorilere eklemek için giriş yapmalısınız.")
        return redirect('giris_yap')
    
    dukkan = get_object_or_404(Dukkan, id=id)
    favori, created = Favori.objects.get_or_create(kullanici=request.user, dukkan=dukkan)
    
    if not created:
        favori.delete() # Varsa sil (Tıklayınca çıkar)
    
    return redirect('dukkan_detay', id=id)
# --- AI ARIZA TESPİT API ---
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ai_ariza_tespit(request):
    if request.method != "POST":
        return JsonResponse({"hata": "POST isteği gönderilmeli"}, status=400)

    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"hata": "JSON formatı hatalı"}, status=400)

    sikayet = data.get("sikayet", "")
    belirtiler = data.get("belirtiler", [])
    marka_model = data.get("marka_model", "")
    km = data.get("km", None)
    yakit = data.get("yakit", "")

    # Basit kural tabanlı yapay zeka
    olasi_arizalar = []

    if "titreme" in sikayet.lower():
        olasi_arizalar.append({
            "ariza": "Motor Ateşleme Problemi",
            "aciklama": "Bobin, buji veya enjektör kaynaklı olabilir.",
            "oneri": "Ateşleme sistemi kontrol edilmeli."
        })

    if "hararet" in sikayet.lower() or "ısı" in sikayet.lower():
        olasi_arizalar.append({
            "ariza": "Soğutma Sistemi Problemi",
            "aciklama": "Radyatör, termostat veya devirdaim pompası olabilir.",
            "oneri": "Soğutma sıvısı ve sensörler kontrol edilmeli."
        })

    if "çalışmıyor" in sikayet.lower() or "marş" in sikayet.lower():
        olasi_arizalar.append({
            "ariza": "Marş - Akü Problemi",
            "aciklama": "Zayıf akü, marş motoru veya şarj dinamosu.",
            "oneri": "Akü ve marş sistemi voltaj testi yapılmalı."
        })

    # Eğer hiç eşleşme yoksa genel bir öneri
    if not olasi_arizalar:
        olasi_arizalar.append({
            "ariza": "Genel Kontrol Önerisi",
            "aciklama": "Belirtiler net değil, detaylı kontrol gerekli.",
            "oneri": "Güvenilir bir serviste teşhis yapılmalı."
        })

    return JsonResponse({
        "durum": "başarılı",
        "tahmin_sayisi": len(olasi_arizalar),
        "tahminler": olasi_arizalar,
    })
