"""
QuoteService — Orchestration de la création et gestion des devis.
"""
import logging
import secrets
from decimal import Decimal

from .pricing_service import PricingService

logger = logging.getLogger(__name__)


class QuoteService:

    def __init__(self):
        self.pricing_service = PricingService()

    def create_from_wizard(self, validated_data: dict):
        """
        Crée un devis complet depuis les données du wizard.

        1. Charge les FK depuis la DB
        2. Calcule les prix via PricingService
        3. Crée le Quote
        4. Crée/met à jour le Lead
        5. Retourne le quote

        Args:
            validated_data: dict validé par QuoteCreateSerializer

        Returns:
            Quote instance
        """
        from quotes.models import Quote
        from services_catalog.models import ProjectType, DesignOption, ComplexityLevel, SupplementaryOption

        # 1. Charger les FK
        from rest_framework.exceptions import ValidationError
        try:
            project_type = ProjectType.objects.get(pk=validated_data['project_type_id'])
        except ProjectType.DoesNotExist:
            raise ValidationError({'project_type_id': 'Type de projet invalide.'})
        design_option = None
        if validated_data.get('design_option_id'):
            try:
                design_option = DesignOption.objects.get(pk=validated_data['design_option_id'])
            except DesignOption.DoesNotExist:
                raise ValidationError({'design_option_id': 'Option design invalide.'})
        complexity = None
        if validated_data.get('complexity_id'):
            try:
                complexity = ComplexityLevel.objects.get(pk=validated_data['complexity_id'])
            except ComplexityLevel.DoesNotExist:
                raise ValidationError({'complexity_id': 'Niveau de complexité invalide.'})
        option_ids = validated_data.get('option_ids', [])
        options = list(SupplementaryOption.objects.filter(pk__in=option_ids)) if option_ids else []

        # 2. Calcul des prix
        from company.models import CompanySettings
        settings = CompanySettings.get()
        vat_rate = Decimal(str(settings.vat_rate))

        pricing = PricingService.full_breakdown(
            project_type=project_type,
            design_option=design_option,
            complexity=complexity,
            options=options,
            discount_percent=Decimal(str(validated_data.get('discount_percent', 0))),
            vat_rate=vat_rate,
        )

        # 3. Créer le Quote
        quote = Quote(
            project_type=project_type,
            design_option=design_option,
            complexity=complexity,
            client_name=validated_data['client_name'],
            client_email=validated_data['client_email'],
            client_phone=validated_data.get('client_phone', ''),
            client_company=validated_data.get('client_company', ''),
            project_description=validated_data.get('project_description', ''),
            desired_deadline=validated_data.get('desired_deadline'),
            signature_token=secrets.token_urlsafe(32),
            **pricing,
        )
        quote.save()

        if options:
            quote.options.set(options)

        # Lead capture is handled by post_save signal in quotes/signals.py (SRP)

        return quote

    def calculate_price_preview(self, data: dict) -> dict:
        """
        Calcul de prix sans persistance en DB.
        Utilisé pour /price-preview/ endpoint.
        """
        from services_catalog.models import ProjectType, DesignOption, ComplexityLevel, SupplementaryOption

        from rest_framework.exceptions import ValidationError
        try:
            project_type = ProjectType.objects.get(pk=data['project_type_id'])
        except ProjectType.DoesNotExist:
            raise ValidationError({'project_type_id': 'Type de projet invalide.'})
        try:
            design_option = DesignOption.objects.get(pk=data['design_option_id']) if data.get('design_option_id') else None
        except DesignOption.DoesNotExist:
            raise ValidationError({'design_option_id': 'Option design invalide.'})
        try:
            complexity = ComplexityLevel.objects.get(pk=data['complexity_id']) if data.get('complexity_id') else None
        except ComplexityLevel.DoesNotExist:
            raise ValidationError({'complexity_id': 'Niveau de complexité invalide.'})
        option_ids = data.get('option_ids', [])
        options = list(SupplementaryOption.objects.filter(pk__in=option_ids)) if option_ids else []

        from company.models import CompanySettings
        settings = CompanySettings.get()

        return PricingService.full_breakdown(
            project_type=project_type,
            design_option=design_option,
            complexity=complexity,
            options=options,
            discount_percent=Decimal('0'),
            vat_rate=Decimal(str(settings.vat_rate)),
        )
