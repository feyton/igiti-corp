import os

from decouple import config

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.localhost']

SECRET_KEY = config('SECRET_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL SETTINGS
EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'feytonf@gmail.com'
EMAIL_HOST_PASSWORD = 'Fahrer25.06.'
EMAIL_USE_SSL =False

STRIPE_PUBLISHABLE_KEY = 'pk_test_Eu2FdXltbLeQuxQNotWjW7Mt003XiV535O'
STRIPE_SECRET_KEY = 'sk_test_5HwDjlXprokf1GPBHmxkHyrQ00tO0QvJqT'


# DATABASES

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
    ]
STATIC_ROOT = (os.path.join(BASE_DIR, 'asset'))
STATIC_URL = '/static/'


# media root folder
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SITE_ID = 1