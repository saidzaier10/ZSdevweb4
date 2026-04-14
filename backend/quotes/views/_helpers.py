from django.utils.crypto import constant_time_compare


def is_token_valid(provided_token: str, expected_token: str) -> bool:
    """Compare les tokens de façon sûre (résiste aux attaques timing)."""
    if not provided_token or not expected_token:
        return False
    return constant_time_compare(str(provided_token), str(expected_token))
