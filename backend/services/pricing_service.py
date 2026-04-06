"""
PricingService — Calculs de prix PURS (aucun appel ORM).

Le caller charge les objets depuis la DB et les passe en paramètre.
Toutes les méthodes sont statiques ou classmethods pour faciliter les tests.
"""
from decimal import Decimal, ROUND_HALF_UP


class PricingService:

    @staticmethod
    def _to_decimal(value) -> Decimal:
        """Convertit en Decimal proprement."""
        if value is None:
            return Decimal('0')
        return Decimal(str(value))

    @staticmethod
    def calculate_base(project_type) -> Decimal:
        return Decimal(str(project_type.base_price))

    @staticmethod
    def apply_design_supplement(design_option) -> Decimal:
        if design_option is None:
            return Decimal('0')
        return Decimal(str(design_option.price_supplement))

    @staticmethod
    def apply_complexity(subtotal: Decimal, complexity) -> Decimal:
        if complexity is None:
            return subtotal
        return (subtotal * Decimal(str(complexity.multiplier))).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    @staticmethod
    def calculate_options_total(options) -> Decimal:
        if not options:
            return Decimal('0')
        return sum(Decimal(str(o.price)) for o in options)

    @staticmethod
    def apply_discount(subtotal: Decimal, discount_percent: Decimal) -> tuple:
        """Retourne (subtotal_net, discount_amount)."""
        if discount_percent <= 0:
            return subtotal, Decimal('0')
        discount_amount = (subtotal * discount_percent / 100).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        return subtotal - discount_amount, discount_amount

    @staticmethod
    def apply_vat(subtotal_ht: Decimal, vat_rate: Decimal = Decimal('20')) -> Decimal:
        return (subtotal_ht * vat_rate / 100).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    @staticmethod
    def calculate_installments(total_ttc: Decimal) -> dict:
        """Plan de paiement 30/40/30."""
        installment_1 = (total_ttc * Decimal('0.30')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        installment_2 = (total_ttc * Decimal('0.40')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # Le 3ème acompte = total - (1 + 2) pour éviter les erreurs d'arrondi
        installment_3 = total_ttc - installment_1 - installment_2
        return {
            'installment_1': installment_1,
            'installment_2': installment_2,
            'installment_3': installment_3,
        }

    @classmethod
    def full_breakdown(
        cls,
        project_type,
        design_option=None,
        complexity=None,
        options=None,
        discount_percent: Decimal = Decimal('0'),
        vat_rate: Decimal = Decimal('20'),
    ) -> dict:
        """
        Calcul complet de la tarification.

        Args:
            project_type: instance ProjectType (doit avoir base_price)
            design_option: instance DesignOption ou None
            complexity: instance ComplexityLevel ou None
            options: queryset ou liste de SupplementaryOption
            discount_percent: remise en % (ex: 10 pour 10%)
            vat_rate: taux TVA (20 par défaut)

        Returns:
            dict avec tous les champs prix prêts à stamper sur Quote
        """
        discount_percent = Decimal(str(discount_percent))
        vat_rate = Decimal(str(vat_rate))

        # 1. Prix de base
        base_price = cls.calculate_base(project_type)

        # 2. Supplément design
        design_supplement = cls.apply_design_supplement(design_option)
        after_design = base_price + design_supplement

        # 3. Multiplicateur complexité
        complexity_factor = Decimal(str(complexity.multiplier)) if complexity else Decimal('1')
        after_complexity = cls.apply_complexity(after_design, complexity)

        # 4. Options supplémentaires
        options_total = cls.calculate_options_total(options or [])

        # 5. Sous-total avant remise
        subtotal_before_discount = after_complexity + options_total

        # 6. Remise
        subtotal_ht, discount_amount = cls.apply_discount(subtotal_before_discount, discount_percent)

        # 7. TVA
        vat_amount = cls.apply_vat(subtotal_ht, vat_rate)

        # 8. Total TTC
        total_ttc = subtotal_ht + vat_amount

        # 9. Plan de paiement
        installments = cls.calculate_installments(total_ttc)

        return {
            'base_price': base_price,
            'design_supplement': design_supplement,
            'complexity_factor': complexity_factor,
            'options_total': options_total,
            'subtotal_ht': subtotal_ht,
            'discount_percent': discount_percent,
            'discount_amount': discount_amount,
            'vat_rate': vat_rate,
            'vat_amount': vat_amount,
            'total_ttc': total_ttc,
            **installments,
        }

    @classmethod
    def quick_estimate(cls, base_price: float, complexity_multiplier: float = 1.0) -> dict:
        """
        Estimation rapide sans objet DB.
        Utilisé pour le simulateur frontend (pas d'auth requise).
        """
        base = Decimal(str(base_price))
        multiplier = Decimal(str(complexity_multiplier))
        ht = (base * multiplier).quantize(Decimal('0.01'))
        vat = cls.apply_vat(ht)
        ttc = ht + vat
        return {
            'subtotal_ht': ht,
            'vat_amount': vat,
            'total_ttc': ttc,
            **cls.calculate_installments(ttc),
        }
