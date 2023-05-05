from .base import *
import sys

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "interface.amovil.co",
    "interface.amovil.com.co",
    "interfacep.amovil.com.co",
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
]
CSRF_TRUSTED_ORIGINS = [
    "https://interface.amovil.com.co",
    "http://interfacep.amovil.com.co",
    "https://interfacep.amovil.com.co",
    "http://127.0.0.1",
    "http://localhost",
    "http://0.0.0.0"
]

CSRF_COOKIE_SECURE = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_ENGINE = get_secret("DB_ENGINE")
DB_USERNAME = get_secret("DB_USERNAME")
DB_PASS = get_secret("DB_PASS")
DB_HOST = get_secret("DB_HOST")
DB_PORT = get_secret("DB_PORT")
DB_NAME = get_secret("DB_NAME")

if DB_ENGINE and DB_NAME and DB_USERNAME:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends." + DB_ENGINE,
            "NAME": DB_NAME,
            "USER": DB_USERNAME,
            "PASSWORD": DB_PASS,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db.sqlite3",
        }
    }
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR.child("static")]
STATIC_ROOT = BASE_DIR.child("staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.child("media")

# EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = get_secret("EMAIL")
EMAIL_HOST_PASSWORD = get_secret("PASS_EMAIL")
EMAIL_PORT = 587

sys.path.append(BASE_DIR.child("scripts"))
sys.path.append(BASE_DIR.child("scripts", "extrae_bi"))
