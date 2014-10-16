DEBUG = False

STATIC_ROOT = 'static/'

ALLOWED_HOSTS = (
    'werwer.aetherclub.be',
)

# Oauth client config
OAUTH2_CLIENT_SETTINGS = {
    'client_id': 'werwer-prod',
    'oauth2_endpoint': 'http://werwer.aetherclub.be/oauth2/authorize',
}
