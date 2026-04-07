import pytest
from rest_framework import serializers

from utils.email_validation import validate_business_email


def test_validate_business_email_accepts_standard_domain():
    assert validate_business_email('client@example.com') == 'client@example.com'


def test_validate_business_email_rejects_disposable_domain():
    with pytest.raises(serializers.ValidationError):
        validate_business_email('test@mailinator.com')
