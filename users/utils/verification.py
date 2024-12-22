import random
from django.core.cache import cache


def generate_verification_code(user_id):
    """
    Generate a 6-digit verification code and cache it for a user.

    The code is stored in the cache for 10 minutes along with
    the user's associated ID for verification purposes.

    Args:
        user_id (int): The ID of the user for whom the code is generated.

    Returns:
        str: The generated 6-digit verification code.
    """
    code = f"{random.randint(100000, 999999)}"
    cache_key = f"verification_code_{user_id}"
    cache.set(cache_key, code, timeout=600)

    code_key = f"user_id_for_code_{code}"
    cache.set(code_key, user_id, timeout=600)

    return code
