import random
import string
from django.utils.deconstruct import deconstructible


@deconstructible
class GenerateToken(object):
    def __init__(self, token_length):
        self.token_length = token_length

    def __call__(self, *args, **kwargs):
        return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(self.token_length))

    def __eq__(self, other):
        return self.token_length == other.token_length

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
