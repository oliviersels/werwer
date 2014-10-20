import random
import string

def generate_token_func(length):
    return lambda: ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(length))
