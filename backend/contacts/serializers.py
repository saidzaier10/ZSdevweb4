from rest_framework import serializers
from .models import ContactRequest
from utils.email_validation import validate_business_email


class ContactRequestSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        return validate_business_email(value)

    class Meta:
        model = ContactRequest
        fields = ('name', 'email', 'phone', 'company', 'subject', 'message')
