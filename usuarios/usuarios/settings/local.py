from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('USER'),
        'PASSWORD': get_secret('PASSWORD'),
        'HOST': 'localhost',
        'PORT':'5432',
    }
}

STATIC_URL = 'static/'

#ARCHIVOS ESTATICOS
STATICFILES_DIRS = [BASE_DIR.child('static')]

#ARCHIVOS ESTATICOS MULTIMEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')

#EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587