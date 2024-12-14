import random
from django.core.cache import cache


def generate_verification_code(user_id):
    """
    Generate a 6-digit verification code and store it in the cache.
    """
    code = f"{random.randint(100000, 999999)}"
    cache_key = f"verification_code_{user_id}"
    cache.set(cache_key, code, timeout=600)
    return code


def fetch_verification_code(user_id):
    """
    Retrieve the verification code from the cache.
    """
    cache_key = f"verification_code_{user_id}"
    return cache.get(cache_key)
