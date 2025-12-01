from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

# 1. DÜKKAN MODELİ
class Dukkan(models.Model):
    KATEGORILER = (
        ('MOTOR', 'Motor ve Mekanik'),
        ('BAKIM', 'Periyodik Bakım & Yağ'),
        ('ELEKTRIK', 'Oto Elektrik ve Beyin'),
        ('AKU', 'Akü Satış & Değişim'),
        ('KAPORTA', 'Kaporta ve Boya'),
        ('LASTIK', 'Lastik ve Jant'),
        ('YEDEK', 'Yedek Parça'),
        ('EGZOZ', 'Egzoz ve Emisyon'),
        ('TORNACI', 'Torna ve Tesviye'),
        ('YOLYARDIM', 'Yol Yardım & Çekici'),
        ('EKSPERTIZ', 'Oto Ekspertiz'),
        ('DOSEME', 'Oto Döşeme & Kılıf'),
        ('KILIT', 'Oto Kilit & Anahtar'),
    )

    SINIF_SECENEKLERI = (
        ('EKONOMIK', 'Ekonomik - Bütçe Dostu'),
        ('STANDART', 'Standart - Fiyat/Performans'),
        ('PREMIUM', 'Premium - Orijinal Parça & Yetkili Kalitesi'),
    )

    isim = models.CharField(max_length=200, verbose_name="Dükkan Adı")
    kategori = models.CharField(max_length=50, choices=KATEGORILER, verbose_name="Kategori")
    hizmet_sinifi = models.CharField(max_length=20, choices=SINIF_SECENEKLERI, default='STANDART', verbose_name="Hizmet Sınıfı")
    uzmanlik = models.CharField(max_length=300, verbose_name="Uzmanlık (Örn: Sadece BMW bakar)")
    telefon = models.CharField(max_length=20, verbose_name="Telefon Numarası")
    adres = models.TextField(verbose_name="Açık Adres")
    konum_linki = models.URLField(max_length=850, blank=True, verbose_name="Google Harita Linki")
    foto = models.ImageField(upload_to='dukkanlar/', verbose_name="Dükkan Fotosu", blank=True, null=True)
    
    # PREMIUM & ONAY
    onayli_esnaf = models.BooleanField(default=False, verbose_name="Mavi Tik (Güvenilir Esnaf)")
    vitrin_uye = models.BooleanField(default=False, verbose_name="Vitrin Üye (En Üstte Çıkar)")
    yayinda = models.BooleanField(default=False, verbose_name="Yayında mı? (Onay)")

    # İSTATİSTİK
    goruntulenme = models.IntegerField(default=0, verbose_name="Görüntülenme Sayısı")

    # EK ÖZELLİKLER
    kredi_karti = models.BooleanField(default=False, verbose_name="Kredi Kartı Geçerli")
    bekleme_salonu = models.BooleanField(default=False, verbose_name="Bekleme Salonu Var")
    nobetci = models.BooleanField(default=False, verbose_name="7/24 Açık / Nöbetçi")
    ikame_arac = models.BooleanField(default=False, verbose_name="İkame Araç Veriyor")

    # >>> YENİ: KAMPANYA SİSTEMİ <<<
    kampanya_baslik = models.CharField(max_length=100, blank=True, verbose_name="Kampanya Başlığı (Örn: Kış İndirimi)")
    kampanya_detay = models.CharField(max_length=255, blank=True, verbose_name="Kampanya Detayı (Örn: Tüm akülerde %20 indirim)")

    def __str__(self):
        return self.isim

    @property
    def ortalama_puan(self):
        avg = self.yorumlar.aggregate(Avg('puan'))['puan__avg']
        return round(avg, 1) if avg else 0

    @property
    def yorum_sayisi(self):
        return self.yorumlar.count()

    class Meta:
        verbose_name_plural = "Sanayi Esnafları"


# 2. YORUM MODELİ
class Yorum(models.Model):
    dukkan = models.ForeignKey(Dukkan, on_delete=models.CASCADE, related_name='yorumlar')
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    puan = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)]) 
    metin = models.TextField(verbose_name="Yorumunuz")
    tarih = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.kullanici.username} - {self.dukkan.isim}"
    
    class Meta:
        ordering = ['-tarih']


# 3. ARAÇ (GARAJ) MODELİ
class Arac(models.Model):
    YAKIT_TIPLERI = (('dizel', 'Dizel'), ('benzin', 'Benzin/LPG'), ('elektrik', 'Elektrik'))
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE)
    marka_model = models.CharField(max_length=100, verbose_name="Marka & Model")
    yil = models.IntegerField(verbose_name="Model Yılı", default=2015)
    km = models.IntegerField(verbose_name="Güncel Kilometre")
    son_bakim_km = models.IntegerField(verbose_name="Son Bakım KM", blank=True, null=True)
    yakit = models.CharField(max_length=20, choices=YAKIT_TIPLERI, default='dizel')

    def __str__(self):
        return f"{self.kullanici.username} - {self.marka_model}"


# 4. FAVORİ MODELİ
class Favori(models.Model):
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)
    dukkan = models.ForeignKey(Dukkan, on_delete=models.CASCADE)
    tarih = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('kullanici', 'dukkan')
        verbose_name_plural = "Favoriler"

    def __str__(self):
        return f"{self.kullanici.username} -> {self.dukkan.isim}"