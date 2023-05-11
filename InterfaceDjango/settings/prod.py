from .base import *
import sys


ALLOWED_HOSTS = [
    "https://interface.amovil.com.co",
    "http://interfacep.amovil.com.co",
    "https://interfacep.amovil.com.co",
    "http://127.0.0.1",
    "http://localhost",
    "http://0.0.0.0"
]

RENDER_EXTERNAL_HOSTNAME = get_secret("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # This is equivalent to 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


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
STATIC_ROOT = BASE_DIR.child("code","staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.child("media")

# EMAIL SETTINGS
ADMINS = [('Augusto', 'cetrusa@hotmail.com'),]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = get_secret("EMAIL")
EMAIL_HOST_PASSWORD = get_secret("PASS_EMAIL")
EMAIL_PORT = 587

sys.path.append(BASE_DIR.child("scripts"))
sys.path.append(BASE_DIR.child("scripts", "extrae_bi"))


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'root': {
        'handlers': ['mail_admins'],
        'level': 'ERROR'
    }
}
