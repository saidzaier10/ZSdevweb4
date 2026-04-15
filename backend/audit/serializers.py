import ipaddress
from urllib.parse import urlparse

from rest_framework import serializers

from utils.email_validation import validate_business_email

from .models import AuditRequest

_BLOCKED_HOSTNAMES = frozenset({
    'localhost', '127.0.0.1', '0.0.0.0', '::1',
    '169.254.169.254',  # AWS metadata
    'metadata.google.internal',
})


class AuditRequestSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        return validate_business_email(value)

    def validate_site_url(self, value):
        """Refuse les URLs internes/SSRF."""
        try:
            parsed = urlparse(value)
            hostname = (parsed.hostname or '').lower()
        except Exception:
            raise serializers.ValidationError('URL invalide.')

        if not hostname:
            raise serializers.ValidationError('URL invalide.')

        if hostname in _BLOCKED_HOSTNAMES:
            raise serializers.ValidationError('Cette URL ne peut pas être auditée.')

        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                raise serializers.ValidationError('Les adresses IP internes ne sont pas autorisées.')
        except ValueError:
            pass  # Nom de domaine — OK

        return value

    class Meta:
        model = AuditRequest
        fields = ('name', 'email', 'phone', 'company', 'site_url',
                  'current_issues', 'objectives', 'budget_range',
                  'timeline', 'additional_info')
