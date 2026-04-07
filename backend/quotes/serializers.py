from rest_framework import serializers
from .models import Quote, QuoteEmailLog
from utils.email_validation import validate_business_email
from services_catalog.serializers import (
    ProjectTypeSerializer, DesignOptionSerializer,
    ComplexityLevelSerializer, SupplementaryOptionSerializer
)


class QuoteCreateSerializer(serializers.Serializer):
    """Validation des données du wizard de devis."""
    project_type_id = serializers.IntegerField()
    design_option_id = serializers.IntegerField(required=False, allow_null=True)
    complexity_id = serializers.IntegerField(required=False, allow_null=True)
    option_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list
    )

    client_name = serializers.CharField(max_length=200)
    client_email = serializers.EmailField()
    client_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    client_company = serializers.CharField(max_length=200, required=False, allow_blank=True)
    project_description = serializers.CharField(required=False, allow_blank=True)
    desired_deadline = serializers.DateField(required=False, allow_null=True)
    discount_percent = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False, default=0,
        min_value=0, max_value=100,
    )

    def validate_client_email(self, value):
        return validate_business_email(value)


class QuoteListSerializer(serializers.ModelSerializer):
    project_type_name = serializers.CharField(source='project_type.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Quote
        fields = (
            'uuid', 'quote_number', 'client_name', 'client_email',
            'project_type_name', 'total_ttc', 'status', 'status_display',
            'created_at', 'valid_until',
        )


class QuoteDetailSerializer(serializers.ModelSerializer):
    project_type = ProjectTypeSerializer(read_only=True)
    design_option = DesignOptionSerializer(read_only=True)
    complexity = ComplexityLevelSerializer(read_only=True)
    options = SupplementaryOptionSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)

    class Meta:
        model = Quote
        fields = (
            'uuid', 'quote_number',
            'project_type', 'design_option', 'complexity', 'options',
            'client_name', 'client_email', 'client_phone', 'client_company',
            'project_description', 'desired_deadline',
            'base_price', 'design_supplement', 'complexity_factor',
            'options_total', 'subtotal_ht', 'discount_percent', 'discount_amount',
            'vat_rate', 'vat_amount', 'total_ttc',
            'installment_1', 'installment_2', 'installment_3',
            'status', 'status_display', 'valid_until', 'is_expired',
            'created_at', 'updated_at',
        )


class PricePreviewSerializer(serializers.Serializer):
    """Calcul de prix sans persistance."""
    project_type_id = serializers.IntegerField()
    design_option_id = serializers.IntegerField(required=False, allow_null=True)
    complexity_id = serializers.IntegerField(required=False, allow_null=True)
    option_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list
    )
