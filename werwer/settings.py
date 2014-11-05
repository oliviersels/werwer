"""
Django settings for werwer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tcj3ofxicx_+9u4%lwd3_t^f-h3r7++z-7z%&p*6ci^(q#59@c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'oauth2_provider',

    'werapp',
    'wersite',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'werwer.urls'

WSGI_APPLICATION = 'werwer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# Should be set in local.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('RDS_DB_NAME', ''),
        'USER': os.environ.get('RDS_USERNAME', ''),
        'PASSWORD': os.environ.get('RDS_PASSWORD', ''),
        'HOST': os.environ.get('RDS_HOSTNAME', ''),
        'PORT': os.environ.get('RDS_PORT', ''),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

from django.utils.translation import ugettext_lazy as _

LANGUAGES = (
    ('nl', _('Dutch')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    'locale',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'werapp.Player'

# Celery
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Template dirs
TEMPLATE_DIRS = (
)

# Rest framework config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# Oauth client config
OAUTH2_CLIENT_SETTINGS = {
    'client_id': 'werwer-dev',
    'oauth2_endpoint': 'http://localhost:8000/oauth2/authorize',
}

# Add a settings to get the current HOST_NAME (I don't use contrib.sites because it is overkill.
# HOST_NAME = '' # You should set this in local.py and production.py

# RECAPTCHA settings
RECAPTCHA_PUBLIC_KEY = '6Lc-UvwSAAAAACP7r68zWfuQeMXR83km8GZRIDrJ'
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + ("django.core.context_processors.request",)

try:
    from local import *
except ImportError:
    pass

GLOBAL_CONFIG = os.environ.get('GLOBAL_CONFIG', 'dev')

if GLOBAL_CONFIG == 'prod':
    try:
        from production import *
    except ImportError:
        pass
