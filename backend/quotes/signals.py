"""
Signaux Django pour l'app quotes.

SRP: QuoteService ne s'occupe plus de capturer le lead.
     Ce signal gère cette responsabilité de façon découplée.
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_save, sender='quotes.Quote')
def capture_lead_on_quote_created(sender, instance, created, **kwargs):
    """
    À la création d'un Quote, capture ou met à jour le lead associé.
    Découplé de QuoteService — ne bloque jamais la création du devis.
    """
    if not created:
        return

    # Si le lead est déjà associé (ex: créé manuellement en admin), on skip
    if instance.lead_id:
        return

    try:
        from services.lead_service import LeadService

        lead_service = LeadService()
        lead, _ = lead_service.capture(
            email=instance.client_email,
            source='quote_wizard',
            name=instance.client_name,
            phone=instance.client_phone or '',
            company=instance.client_company or '',
            project_type_id=instance.project_type_id,
        )
        # Mise à jour sans déclencher le signal à nouveau
        sender.objects.filter(pk=instance.pk).update(lead=lead)
        instance.lead = lead

    except Exception as e:
        logger.warning(
            f'Signal: lead capture failed for quote {instance.quote_number} '
            f'(non-blocking): {e}'
        )
