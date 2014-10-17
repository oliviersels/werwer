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
