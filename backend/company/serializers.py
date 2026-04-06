from rest_framework import serializers
from .models import CompanySettings


class CompanySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySettings
        fields = ('company_name', 'tagline', 'description', 'email', 'phone',
                  'address', 'city', 'country', 'logo', 'social_linkedin',
                  'social_github', 'social_twitter', 'vat_rate',
                  'quote_validity_days')
