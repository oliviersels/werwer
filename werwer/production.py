import os

DEBUG = False

STATIC_ROOT = 'static/'

ALLOWED_HOSTS = (
    'aetherclub.be',
    'www.aetherclub.be',
)

# Oauth client config
OAUTH2_CLIENT_SETTINGS = {
    'client_id': 'werwer-prod',
    'oauth2_endpoint': 'http://aetherclub.be/oauth2/authorize',
}

# Celery
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('SMTP_USERNAME', '')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'olivier.sels@gmail.com'

HOST_NAME = 'aetherclub.be'

SERVER_EMAIL = 'olivier.sels@gmail.com'


# Sentry settings
RAVEN_CONFIG = {
    'dsn': 'http://018b8249b7744d65bf1957c45a38f562:43854855bca8425d87463f81072e77a9@sentry.aetherclub.be/2',
}

# Logging via sentry
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
