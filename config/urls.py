from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# DİKKAT: En sona 'favori_islem' eklendi
from rehber.views import home, dukkan_detay, kayit_ol, giris_yap, cikis_yap, esnaf_kayit, profil, favori_islem

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dukkan/<int:id>/', dukkan_detay, name='dukkan_detay'),
    
    # Üyelik
    path('kayit/', kayit_ol, name='kayit_ol'),
    path('giris/', giris_yap, name='giris_yap'),
    path('cikis/', cikis_yap, name='cikis_yap'),
    
    # Esnaf ve Profil
    path('esnaf-kayit/', esnaf_kayit, name='esnaf_kayit'),
    path('profil/', profil, name='profil'),

    # >>> YENİ EKLENEN FAVORI LİNKİ BURADA <<<
    path('favori/<int:id>/', favori_islem, name='favori_islem'),

    # Şifre Sıfırlama
    path('sifre-sifirla/', auth_views.PasswordResetView.as_view(template_name='sifre_sifirla.html'), name='password_reset'),
    path('sifre-sifirla/gonderildi/', auth_views.PasswordResetDoneView.as_view(template_name='sifre_sifirla_bitti.html'), name='password_reset_done'),
    path('sifre-sifirla/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='sifre_sifirla_onayla.html'), name='password_reset_confirm'),
    path('sifre-sifirla/tamamlandi/', auth_views.PasswordResetCompleteView.as_view(template_name='sifre_sifirla_tamam.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)