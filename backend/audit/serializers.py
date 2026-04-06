from rest_framework import serializers
from .models import AuditRequest


class AuditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditRequest
        fields = ('name', 'email', 'phone', 'company', 'site_url',
                  'current_issues', 'objectives', 'budget_range',
                  'timeline', 'additional_info')
