import os
import dj_database_url # Render'ın veritabanı ayarlarını otomatikleştirmek için
from pathlib import Path

# Proje ana dizini
BASE_DIR = Path(__file__).resolve().parent.parent

# Güvenlik Anahtarı (Canlı ortamda güvenlik için dışarıdan çekilir)
# Şimdilik sabit kalsın, Render'da bunu değiştireceğiz.
SECRET_KEY = 'django-insecure-ustam-cepte-key-RENDER-READY'

# Hata Modu (Canlıda KAPALI OLMALI)
DEBUG = os.environ.get('RENDER_DEBUG') == 'True' # Render'a göre True/False olsun

# Host İzinleri (DİKKAT: Türkçe karakterli domain için özel ayar)
# Tüm adreslere izin ver (Yıldız işareti)
ALLOWED_HOSTS = ['*']


RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Uygulamalar
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rehber', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Statik dosyalar için eklendi
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Veritabanı Ayarları (RENDER OTOMATİK VERİTABANI İÇİN)
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}


# Dil ve Saat Ayarları
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

# Statik ve Medya Dosyaları (Whitenoise için)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # Statik dosyaların toplanacağı yer
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'