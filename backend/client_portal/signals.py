import logging

logger = logging.getLogger(__name__)


def on_project_update_created(sender, instance, created, **kwargs):
    """
    Déclenche l'envoi d'un email au client quand une mise à jour visible est créée.
    Importé et connecté dans ClientPortalConfig.ready().
    """
    if not created:
        return
    if not instance.is_visible_to_client:
        return

    from .tasks import notify_client_project_update
    notify_client_project_update.delay(instance.pk)


def on_client_project_saved(sender, instance, created, **kwargs):
    """
    Quand un ClientProject est lié à un devis (à la création ou mise à jour),
    attache automatiquement le PDF du devis comme ProjectDocument de type 'quote'.

    Règle : un seul ProjectDocument par devis (OneToOne via quote_source).
    """
    quote = instance.quote
    if not quote:
        return
    if not quote.pdf_file:
        return

    from .models import ProjectDocument

    # Idempotent : ne crée pas de doublon si déjà lié
    if ProjectDocument.objects.filter(quote_source=quote).exists():
        return

    try:
        ProjectDocument.objects.create(
            project=instance,
            doc_type='quote',
            name=f'Devis {quote.quote_number}',
            file=quote.pdf_file,
            description=f'Devis accepté le {quote.signed_at.strftime("%d/%m/%Y") if quote.signed_at else "—"}',
            quote_source=quote,
        )
        logger.info(
            'portal_document_created quote=%s project_id=%s',
            quote.quote_number, instance.pk,
        )
    except Exception as e:
        logger.error(
            'on_client_project_saved: failed to create ProjectDocument '
            'for quote %s: %s', quote.quote_number, e,
        )
