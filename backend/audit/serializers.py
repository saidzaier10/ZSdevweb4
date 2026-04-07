from rest_framework import serializers
from .models import AuditRequest
from utils.email_validation import validate_business_email


class AuditRequestSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        return validate_business_email(value)

    class Meta:
        model = AuditRequest
        fields = ('name', 'email', 'phone', 'company', 'site_url',
                  'current_issues', 'objectives', 'budget_range',
                  'timeline', 'additional_info')
