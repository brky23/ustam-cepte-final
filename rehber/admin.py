from django.contrib import admin
from .models import Dukkan, Yorum

@admin.register(Dukkan)
class DukkanAdmin(admin.ModelAdmin):
    # LİSTEDE GÖRÜNECEK SÜTUNLAR (Görüntülenme burada!)
    list_display = ('isim', 'kategori', 'telefon', 'goruntulenme', 'yayinda', 'vitrin_uye')
    
    # SAĞ TARAFTAKİ FİLTRELER
    list_filter = ('yayinda', 'kategori', 'vitrin_uye') 
    
    # TIKLAYIP DÜZENLENEBİLECEK ALANLAR
    list_editable = ('yayinda', 'vitrin_uye') 
    
    # ARAMA ÇUBUĞU
    search_fields = ('isim', 'uzmanlik')

@admin.register(Yorum)
class YorumAdmin(admin.ModelAdmin):
    list_display = ('dukkan', 'kullanici', 'puan', 'tarih')