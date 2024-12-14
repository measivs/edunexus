import random
from django.core.cache import cache


def generate_verification_code(user_id):
    """
    Generate a 6-digit verification code and store it in the cache.
    """
    code = f"{random.randint(100000, 999999)}"
    cache_key = f"verification_code_{user_id}"
    cache.set(cache_key, code, timeout=600)

    code_key = f"user_id_for_code_{code}"
    cache.set(code_key, user_id, timeout=600)

    return code
