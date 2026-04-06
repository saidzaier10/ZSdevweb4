"""
LeadService — Capture et scoring des leads.
"""
from django.db.models import F
from django.utils import timezone


class LeadService:
    """
    Score map: définit les points attribués selon les critères.
    """
    SCORE_MAP = {
        'has_phone': 15,
        'has_company': 10,
        'has_name': 5,
        'source_quote_wizard': 25,
        'source_audit_form': 30,
        'source_roi_calculator': 20,
        'source_quick_estimate': 15,
        'source_contact_form': 10,
        'source_simulator': 10,
        'budget_high': 20,       # > 6000€
        'budget_medium': 10,     # 3000-6000€
        'has_project_type': 10,
    }

    SOURCE_SCORE_MAP = {
        'quote_wizard': 25,
        'audit_form': 30,
        'roi_calculator': 20,
        'quick_estimate': 15,
        'contact_form': 10,
        'simulator': 10,
    }

    def capture(self, email: str, source: str, **kwargs) -> tuple:
        """
        Upsert d'un lead par email.
        Score additif (ne diminue jamais).
        Retourne (lead, created).
        """
        from leads.models import Lead

        email = email.lower().strip()

        # Upsert par email (contrainte unique en DB)
        lead, created = Lead.objects.get_or_create(
            email=email,
            defaults={
                'source': source,
                'name': kwargs.get('name', ''),
                'phone': kwargs.get('phone', ''),
                'company': kwargs.get('company', ''),
                'budget_range': kwargs.get('budget_range', ''),
                'notes': kwargs.get('notes', ''),
            }
        )

        if not created:
            # Mettre à jour les champs vides seulement
            update_fields = []
            for field in ('name', 'phone', 'company', 'budget_range'):
                val = kwargs.get(field)
                if val and not getattr(lead, field):
                    setattr(lead, field, val)
                    update_fields.append(field)
            if update_fields:
                lead.save(update_fields=update_fields)

        # Associer le type de projet si fourni
        project_type_id = kwargs.get('project_type_id')
        if project_type_id and not lead.project_type_id:
            lead.project_type_id = project_type_id
            lead.save(update_fields=['project_type_id'])

        # Recalculer et ajouter le score
        new_score = self._calculate_score(lead, source, kwargs)
        if new_score > 0:
            # Score additif — max 100
            Lead.objects.filter(pk=lead.pk).update(
                score=F('score') + new_score
            )
            lead.refresh_from_db()
            if lead.score > 100:
                Lead.objects.filter(pk=lead.pk).update(score=100)
                lead.score = 100

        return lead, created

    def _calculate_score(self, lead, source: str, data: dict) -> int:
        """Calcule les points à AJOUTER (ne recalcule pas tout depuis zéro)."""
        points = 0

        # Source
        points += self.SOURCE_SCORE_MAP.get(source, 0)

        # Données de contact
        if data.get('phone') and not lead.phone:
            points += self.SCORE_MAP['has_phone']
        if data.get('company') and not lead.company:
            points += self.SCORE_MAP['has_company']
        if data.get('name') and not lead.name:
            points += self.SCORE_MAP['has_name']

        # Budget
        budget = data.get('budget_range', '')
        if budget in ('6000-15000', '> 15000'):
            points += self.SCORE_MAP['budget_high']
        elif budget in ('3000-6000',):
            points += self.SCORE_MAP['budget_medium']

        # Type de projet renseigné
        if data.get('project_type_id') and not lead.project_type_id:
            points += self.SCORE_MAP['has_project_type']

        return points

    def mark_converted(self, lead) -> None:
        """
        Marque un lead comme converti (devis accepté).
        LSP: ne réinitialise pas le score — le score reste additif et ne recule jamais.
        """
        if not lead.is_converted:
            lead.is_converted = True
            lead.converted_at = timezone.now()
            lead.save(update_fields=['is_converted', 'converted_at'])
