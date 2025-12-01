from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Dukkan  # <--- İŞTE HATAYI ÇÖZEN SATIR BU!
from .models import Dukkan, Arac
# 1. KULLANICI KAYIT FORMU (E-posta İsteyen)
class KayitFormu(UserCreationForm):
    email = forms.EmailField(required=True, label="E-Posta Adresi")

    class Meta:
        model = User
        fields = ("username", "email")

# 2. ESNAF KAYIT FORMU
class DukkanForm(forms.ModelForm):
    class Meta:
        model = Dukkan
        fields = ['isim', 'kategori', 'uzmanlik', 'telefon', 'adres', 'konum_linki', 'foto']
        
        widgets = {
            'isim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Şampiyon Motor'}),
            'kategori': forms.Select(attrs={'class': 'form-select'}),
            'uzmanlik': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Örn: BMW ve Mercedes motor rektefiye...'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0532 123 45 67'}),
            'adres': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dükkanın açık adresi...'}),
            'konum_linki': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Google Maps linki (Opsiyonel)'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }
# ARAÇ KAYIT FORMU
class AracForm(forms.ModelForm):
    class Meta:
        model = Arac
        fields = ['marka_model', 'yil', 'km', 'son_bakim_km', 'yakit']
        widgets = {
            'marka_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Fiat Egea 1.4'}),
            'yil': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2020'}),
            'km': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '120000'}),
            'son_bakim_km': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '110000'}),
            'yakit': forms.Select(attrs={'class': 'form-select'}),
        }