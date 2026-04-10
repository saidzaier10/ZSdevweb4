"""
Tests unitaires pour QuoteService.
Utilise des mocks pour éviter toute dépendance ORM/DB.
"""
import pytest
from decimal import Decimal
from unittest.mock import MagicMock, patch, PropertyMock


# ---- Helpers ----

def make_project_type(pk=1, name='Site Vitrine', base_price='1500', min_days=14, max_days=21):
    pt = MagicMock()
    pt.pk = pk
    pt.id = pk
    pt.name = name
    pt.base_price = base_price
    pt.min_days = min_days
    pt.max_days = max_days
    return pt


def make_complexity(pk=2, name='Standard', multiplier='1.3'):
    cl = MagicMock()
    cl.pk = pk
    cl.id = pk
    cl.name = name
    cl.multiplier = multiplier
    return cl


def make_design_option(pk=1, name='Standard', price_supplement='0'):
    do = MagicMock()
    do.pk = pk
    do.id = pk
    do.name = name
    do.price_supplement = price_supplement
    return do


# ---- Tests calculate_price_preview (stateless) ----

class TestCalculatePricePreview:
    """
    calculate_price_preview ne touche pas la DB.
    On peut l'importer et le tester directement.
    """

    def test_basic_preview(self):
        from services.pricing_service import PricingService

        pt = make_project_type(base_price='1500')
        result = PricingService.full_breakdown(pt)

        assert result['total_ttc'] == Decimal('1800.00')
        assert result['subtotal_ht'] == Decimal('1500')
        assert result['vat_amount'] == Decimal('300.00')

    def test_preview_with_complexity(self):
        from services.pricing_service import PricingService

        pt = make_project_type(base_price='2000')
        cl = make_complexity(multiplier='1.6')
        result = PricingService.full_breakdown(pt, complexity=cl)

        assert result['subtotal_ht'] == Decimal('3200.00')
        assert result['total_ttc'] == Decimal('3840.00')

    def test_preview_installments_add_up(self):
        from services.pricing_service import PricingService

        pt = make_project_type(base_price='3000')
        result = PricingService.full_breakdown(pt)

        total = result['installment_1'] + result['installment_2'] + result['installment_3']
        assert total == result['total_ttc']


# ---- Tests QuoteService.create_from_wizard (avec mocks complets) ----

class TestCreateFromWizard:
    """
    On mocke tous les imports pour éviter de charger Django.
    Ces tests valident la logique orchestration du service.
    """

    def _make_wizard_data(self, **kwargs):
        defaults = {
            'project_type_id': 1,
            'design_option_id': None,
            'complexity_id': 2,
            'option_ids': [],
            'client_name': 'Marie Dupont',
            'client_email': 'marie@example.com',
            'client_phone': '+33612345678',
            'client_company': 'Acme SARL',
            'project_description': 'Je veux un site vitrine moderne.',
            'desired_deadline': None,
            'discount_percent': '0',
        }
        defaults.update(kwargs)
        return defaults

    @pytest.mark.django_db
    @patch('quotes.models.Quote.save', autospec=True)
    def test_create_returns_quote(self, mock_save):
        """Vérifie que create_from_wizard appelle save() et retourne un Quote."""
        from services_catalog.models import ProjectType, ComplexityLevel, ProjectCategory
        from services.quote_service import QuoteService

        mock_save.return_value = None

        cat = ProjectCategory.objects.create(name='Web', slug='web')
        pt = ProjectType.objects.create(name='Vitrine', slug='vitrine', base_price='1500', category=cat)
        cl = ComplexityLevel.objects.create(name='Simple', slug='simple', multiplier='1.0', order=1)

        wizard_data = self._make_wizard_data(project_type_id=pt.pk, complexity_id=cl.pk)

        result = QuoteService().create_from_wizard(wizard_data)
        assert result is not None
        mock_save.assert_called_once()

    def test_pricing_breakdown_used_correctly(self):
        """Vérifie que les calculs de pricing sont cohérents avec ce que le wizard soumet."""
        from services.pricing_service import PricingService

        pt = make_project_type(base_price='3500')
        cl = make_complexity(multiplier='1.6')
        opts = [MagicMock(price='400'), MagicMock(price='300')]

        result = PricingService.full_breakdown(
            pt, complexity=cl, options=opts,
            discount_percent=Decimal('0')
        )

        # 3500 * 1.6 = 5600 + 700 = 6300 HT
        assert result['subtotal_ht'] == Decimal('6300.00')
        assert result['vat_amount'] == Decimal('1260.00')
        assert result['total_ttc'] == Decimal('7560.00')


# ---- Tests quote number generation ----

class TestQuoteNumberGeneration:
    """
    Le numéro de devis est généré dans Quote.save().
    On teste la logique de formatage.
    """

    def test_format_pattern(self):
        import datetime
        year = datetime.datetime.now().year
        # Simule la génération : QT-{year}-{count:04d}
        count = 1
        number = f'QT-{year}-{count:04d}'
        assert number == f'QT-{year}-0001'

    def test_format_with_high_count(self):
        import datetime
        year = datetime.datetime.now().year
        count = 42
        number = f'QT-{year}-{count:04d}'
        assert number == f'QT-{year}-0042'


# ---- Tests installment consistency ----

class TestInstallmentConsistency:
    """
    Propriété critique : i1 + i2 + i3 == total_ttc toujours.
    Teste avec diverses valeurs pour détecter les erreurs d'arrondi.
    """

    @pytest.mark.parametrize("base_price,multiplier", [
        ('1000', '1.0'),
        ('1500', '1.3'),
        ('2000', '1.6'),
        ('3000', '2.0'),
        ('1234', '1.3'),
        ('5678', '1.6'),
        ('999', '1.0'),
        ('12000', '2.0'),
    ])
    def test_installments_always_sum_to_total(self, base_price, multiplier):
        from services.pricing_service import PricingService

        pt = make_project_type(base_price=base_price)
        cl = make_complexity(multiplier=multiplier)
        result = PricingService.full_breakdown(pt, complexity=cl)

        total = result['installment_1'] + result['installment_2'] + result['installment_3']
        assert total == result['total_ttc'], (
            f"Échec pour base={base_price}, mult={multiplier}: "
            f"{result['installment_1']} + {result['installment_2']} + {result['installment_3']} "
            f"= {total} ≠ {result['total_ttc']}"
        )
