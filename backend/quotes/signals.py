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
def attach_quote_pdf_to_portal(sender, instance, created, **kwargs):
    """
    Quand un devis passe au statut 'accepted' et qu'un ClientProject lui est
    déjà lié, déclenche la création du ProjectDocument côté portail.

    Le signal on_client_project_saved gère la création effective ;
    on l'active ici en cas de race condition (statut accepté avant
    que le projet soit créé — rare, mais possible depuis l'admin).
    """
    if created:
        return
    if instance.status != 'accepted':
        return

    # Utilise le related_name 'project' défini sur ClientProject.quote
    try:
        project = instance.project  # OneToOne reverse accessor
    except Exception:
        return  # Pas encore de ClientProject lié — rien à faire

    if not instance.pdf_file:
        return

    from client_portal.models import ProjectDocument

    if ProjectDocument.objects.filter(quote_source=instance).exists():
        return

    try:
        ProjectDocument.objects.create(
            project=project,
            doc_type='quote',
            name=f'Devis {instance.quote_number}',
            file=instance.pdf_file,
            description=f'Devis accepté le {instance.signed_at.strftime("%d/%m/%Y") if instance.signed_at else "—"}',
            quote_source=instance,
        )
        logger.info(
            'attach_quote_pdf_to_portal: document créé quote=%s project_id=%s',
            instance.quote_number, project.pk,
        )
    except Exception as e:
        logger.error(
            'attach_quote_pdf_to_portal: failed for quote %s: %s',
            instance.quote_number, e,
        )


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
