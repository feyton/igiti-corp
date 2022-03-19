import os

from decouple import config

from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.localhost']


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL SETTINGS
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your email'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_SSL = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SITE_ID = 1
