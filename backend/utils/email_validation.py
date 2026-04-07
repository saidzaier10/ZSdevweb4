from rest_framework import serializers

# Liste volontairement courte pour limiter les faux positifs.
DISPOSABLE_EMAIL_DOMAINS = {
    'mailinator.com',
    'guerrillamail.com',
    '10minutemail.com',
    'temp-mail.org',
    'yopmail.com',
    'sharklasers.com',
}


def validate_business_email(value: str) -> str:
    """Refuse les domaines d'email temporaires les plus courants."""
    if '@' not in value:
        raise serializers.ValidationError('Adresse email invalide.')

    domain = value.rsplit('@', 1)[-1].strip().lower()
    if domain in DISPOSABLE_EMAIL_DOMAINS:
        raise serializers.ValidationError(
            'Les adresses email temporaires ne sont pas acceptées.'
        )

    return value
