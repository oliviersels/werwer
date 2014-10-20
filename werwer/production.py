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
BROKER_URL = 'sqs://'
BROKER_TRANSPORT_OPTIONS = {'region': 'eu-west-1'}
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
