from rest_framework import serializers
from .models import Lead
from utils.email_validation import validate_business_email


class LeadCaptureSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    company = serializers.CharField(max_length=200, required=False, allow_blank=True)
    source = serializers.ChoiceField(choices=Lead.SOURCE_CHOICES)
    budget_range = serializers.ChoiceField(choices=Lead.BUDGET_CHOICES, required=False, allow_blank=True)
    project_type_id = serializers.IntegerField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        return validate_business_email(value)
