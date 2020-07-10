import os

from django.core.exceptions import ImproperlyConfigured

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['notes.igiti.co.rw',
                 'www.notes.igiti.co.rw', "127.0.0.1", "localhost", '198.54.116.172']

# Environment Wrapper


def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ['SECRET_KEY'])


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'igityopp_corp',
        'USER': 'igityopp_fahrer',
        'PASSWORD': get_env_value('DB_PASS'),
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


STRIPE_PUBLISHABLE_KEY = 'LIVE KEYS'
STRIPE_SECRET_KEY = 'LIVE KEYS'

PREPEND_WWW = True
APPEND_SLASH = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = '/home/igityopp/notes.igiti.co.rw/static'
STATIC_URL = '/static/'


# media root folder
MEDIA_ROOT = '/home/igityopp/notes.igiti.co.rw/media'
MEDIA_URL = '/media/'

SITE_ID = 1
# DEPLOYMENT

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = 'admin@igiti.co.rw'
EMAIL_HOST_PASSWORD = 'v1p3k,h@@t'
EMAIL_HOST = '198.54.116.172'
EMAIL_PORT = '465'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
ADMINS = (('Feyton', 'info@igiti.co.rw'),
          ('Fabrice', 'tumbafabruce@gmail.com'))
