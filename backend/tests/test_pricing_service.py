"""
Tests unitaires pour PricingService.
Entièrement purs — aucun accès DB, aucune migration requise.
"""
import pytest
from decimal import Decimal
from unittest.mock import MagicMock

from services.pricing_service import PricingService


def make_project_type(base_price):
    """Crée un mock ProjectType."""
    pt = MagicMock()
    pt.base_price = base_price
    return pt


def make_design_option(price_supplement):
    """Crée un mock DesignOption."""
    do = MagicMock()
    do.price_supplement = price_supplement
    return do


def make_complexity(multiplier):
    """Crée un mock ComplexityLevel."""
    cl = MagicMock()
    cl.multiplier = multiplier
    return cl


def make_option(price, is_recurring=False):
    """Crée un mock SupplementaryOption."""
    opt = MagicMock()
    opt.price = price
    opt.is_recurring = is_recurring
    return opt


# ---- Tests calculate_base ----

class TestCalculateBase:
    def test_integer_price(self):
        pt = make_project_type(1500)
        assert PricingService.calculate_base(pt) == Decimal('1500')

    def test_string_price(self):
        pt = make_project_type('2500.00')
        assert PricingService.calculate_base(pt) == Decimal('2500.00')

    def test_decimal_price(self):
        pt = make_project_type(Decimal('3000.50'))
        assert PricingService.calculate_base(pt) == Decimal('3000.50')


# ---- Tests apply_design_supplement ----

class TestApplyDesignSupplement:
    def test_no_design_option(self):
        assert PricingService.apply_design_supplement(None) == Decimal('0')

    def test_zero_supplement(self):
        do = make_design_option('0.00')
        assert PricingService.apply_design_supplement(do) == Decimal('0.00')

    def test_positive_supplement(self):
        do = make_design_option(500)
        assert PricingService.apply_design_supplement(do) == Decimal('500')


# ---- Tests apply_complexity ----

class TestApplyComplexity:
    def test_no_complexity(self):
        result = PricingService.apply_complexity(Decimal('1000'), None)
        assert result == Decimal('1000')

    def test_multiplier_one(self):
        cl = make_complexity('1.0')
        result = PricingService.apply_complexity(Decimal('1000'), cl)
        assert result == Decimal('1000.00')

    def test_multiplier_1_3(self):
        cl = make_complexity('1.3')
        result = PricingService.apply_complexity(Decimal('1000'), cl)
        assert result == Decimal('1300.00')

    def test_multiplier_2(self):
        cl = make_complexity('2.0')
        result = PricingService.apply_complexity(Decimal('2500'), cl)
        assert result == Decimal('5000.00')

    def test_rounding(self):
        cl = make_complexity('1.3')
        # 1500 * 1.3 = 1950.0 exact
        result = PricingService.apply_complexity(Decimal('1500'), cl)
        assert result == Decimal('1950.00')


# ---- Tests calculate_options_total ----

class TestCalculateOptionsTotal:
    def test_empty_options(self):
        assert PricingService.calculate_options_total([]) == Decimal('0')

    def test_none_options(self):
        assert PricingService.calculate_options_total(None) == Decimal('0')

    def test_single_option(self):
        opts = [make_option(400)]
        assert PricingService.calculate_options_total(opts) == Decimal('400')

    def test_multiple_options(self):
        opts = [make_option(400), make_option(300), make_option(800)]
        assert PricingService.calculate_options_total(opts) == Decimal('1500')


# ---- Tests apply_discount ----

class TestApplyDiscount:
    def test_no_discount(self):
        subtotal_net, discount = PricingService.apply_discount(Decimal('1000'), Decimal('0'))
        assert subtotal_net == Decimal('1000')
        assert discount == Decimal('0')

    def test_10_percent_discount(self):
        subtotal_net, discount = PricingService.apply_discount(Decimal('1000'), Decimal('10'))
        assert discount == Decimal('100.00')
        assert subtotal_net == Decimal('900.00')

    def test_15_percent_discount(self):
        subtotal_net, discount = PricingService.apply_discount(Decimal('2000'), Decimal('15'))
        assert discount == Decimal('300.00')
        assert subtotal_net == Decimal('1700.00')

    def test_negative_discount_treated_as_zero(self):
        # Remise négative ne doit pas augmenter le prix
        subtotal_net, discount = PricingService.apply_discount(Decimal('1000'), Decimal('-5'))
        assert subtotal_net == Decimal('1000')
        assert discount == Decimal('0')


# ---- Tests apply_vat ----

class TestApplyVat:
    def test_standard_20_percent(self):
        vat = PricingService.apply_vat(Decimal('1000'))
        assert vat == Decimal('200.00')

    def test_custom_rate(self):
        vat = PricingService.apply_vat(Decimal('1000'), Decimal('10'))
        assert vat == Decimal('100.00')

    def test_rounding(self):
        # 1001 * 20% = 200.20
        vat = PricingService.apply_vat(Decimal('1001'))
        assert vat == Decimal('200.20')


# ---- Tests calculate_installments ----

class TestCalculateInstallments:
    def test_round_number(self):
        result = PricingService.calculate_installments(Decimal('1200'))
        assert result['installment_1'] == Decimal('360.00')
        assert result['installment_2'] == Decimal('480.00')
        assert result['installment_3'] == Decimal('360.00')

    def test_installments_sum_equals_total(self):
        total = Decimal('3456.78')
        result = PricingService.calculate_installments(total)
        total_check = result['installment_1'] + result['installment_2'] + result['installment_3']
        assert total_check == total, f"Installments ({total_check}) != total ({total})"

    def test_no_floating_point_accumulation(self):
        """Vérifie que i3 = total - i1 - i2 (pas de triple arrondi)."""
        total = Decimal('1000.01')
        result = PricingService.calculate_installments(total)
        assert result['installment_1'] + result['installment_2'] + result['installment_3'] == total


# ---- Tests full_breakdown ----

class TestFullBreakdown:
    def test_minimal_input(self):
        """Juste un type de projet, sans rien d'autre."""
        pt = make_project_type(1500)
        result = PricingService.full_breakdown(pt)

        assert result['base_price'] == Decimal('1500')
        assert result['design_supplement'] == Decimal('0')
        assert result['complexity_factor'] == Decimal('1')
        assert result['options_total'] == Decimal('0')
        assert result['subtotal_ht'] == Decimal('1500')
        assert result['discount_amount'] == Decimal('0')
        assert result['vat_amount'] == Decimal('300.00')
        assert result['total_ttc'] == Decimal('1800.00')

    def test_with_design_option(self):
        pt = make_project_type(1500)
        do = make_design_option(500)
        result = PricingService.full_breakdown(pt, design_option=do)

        assert result['base_price'] == Decimal('1500')
        assert result['design_supplement'] == Decimal('500')
        assert result['subtotal_ht'] == Decimal('2000')
        assert result['total_ttc'] == Decimal('2400.00')

    def test_with_complexity(self):
        pt = make_project_type(1000)
        cl = make_complexity('1.3')
        result = PricingService.full_breakdown(pt, complexity=cl)

        assert result['subtotal_ht'] == Decimal('1300.00')
        assert result['vat_amount'] == Decimal('260.00')
        assert result['total_ttc'] == Decimal('1560.00')

    def test_with_options(self):
        pt = make_project_type(2000)
        opts = [make_option(400), make_option(300)]
        result = PricingService.full_breakdown(pt, options=opts)

        assert result['options_total'] == Decimal('700')
        assert result['subtotal_ht'] == Decimal('2700')

    def test_with_discount(self):
        pt = make_project_type(1000)
        result = PricingService.full_breakdown(pt, discount_percent=Decimal('10'))

        assert result['discount_amount'] == Decimal('100.00')
        assert result['subtotal_ht'] == Decimal('900.00')
        assert result['vat_amount'] == Decimal('180.00')
        assert result['total_ttc'] == Decimal('1080.00')

    def test_full_scenario(self):
        """Scénario complet: vitrine premium avancé + SEO + blog + 10% remise."""
        pt = make_project_type('2500')
        do = make_design_option('500')
        cl = make_complexity('1.3')
        opts = [make_option('400'), make_option('350')]

        result = PricingService.full_breakdown(
            pt, design_option=do, complexity=cl,
            options=opts, discount_percent=Decimal('10')
        )

        # base 2500 + design 500 = 3000
        # * 1.3 = 3900
        # + options 750 = 4650
        # - 10% = 4185
        # + TVA 20% = 5022
        assert result['base_price'] == Decimal('2500')
        assert result['design_supplement'] == Decimal('500')
        assert result['options_total'] == Decimal('750')
        assert result['discount_amount'] == Decimal('465.00')
        assert result['subtotal_ht'] == Decimal('4185.00')
        assert result['vat_amount'] == Decimal('837.00')
        assert result['total_ttc'] == Decimal('5022.00')
        # Vérification installments
        total_inst = result['installment_1'] + result['installment_2'] + result['installment_3']
        assert total_inst == result['total_ttc']

    def test_installments_in_result(self):
        pt = make_project_type(1200)
        result = PricingService.full_breakdown(pt)
        assert 'installment_1' in result
        assert 'installment_2' in result
        assert 'installment_3' in result


# ---- Tests quick_estimate ----

class TestQuickEstimate:
    def test_basic(self):
        result = PricingService.quick_estimate(1000)
        assert result['subtotal_ht'] == Decimal('1000.00')
        assert result['vat_amount'] == Decimal('200.00')
        assert result['total_ttc'] == Decimal('1200.00')

    def test_with_multiplier(self):
        result = PricingService.quick_estimate(1000, 1.5)
        assert result['subtotal_ht'] == Decimal('1500.00')
        assert result['total_ttc'] == Decimal('1800.00')

    def test_installments_present(self):
        result = PricingService.quick_estimate(1000)
        assert 'installment_1' in result
        total_inst = result['installment_1'] + result['installment_2'] + result['installment_3']
        assert total_inst == result['total_ttc']
