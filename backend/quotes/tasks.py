"""
Tâches Celery pour la gestion des devis.

Planning recommandé (à configurer dans l'admin Django > Periodic Tasks) :
  - expire_old_quotes        → chaque jour à 02:00
  - send_quote_reminders     → chaque jour à 09:00
  - send_lead_follow_ups     → chaque jour à 10:00
  - cleanup_draft_quotes     → chaque lundi à 03:00
"""
import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def expire_old_quotes(self):
    """
    Marque comme 'expired' tous les devis dont la date de validité est dépassée.
    Cron recommandé : chaque jour à 02:00.
    """
    from .models import Quote

    try:
        today = timezone.now().date()
        expired = Quote.objects.filter(
            status__in=['draft', 'sent', 'viewed'],
            valid_until__lt=today,
        )
        count = expired.count()
        expired.update(status='expired')
        logger.info(f'expire_old_quotes: {count} devis expirés')
        return {'expired': count}
    except Exception as exc:
        logger.error(f'expire_old_quotes error: {exc}')
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def send_quote_reminders(self):
    """
    Envoie des rappels pour les devis envoyés et non consultés depuis 3 jours,
    et pour les devis consultés mais non acceptés depuis 5 jours.
    Cron recommandé : chaque jour à 09:00.
    """
    from .models import Quote
    from services.email_service import EmailService

    try:
        now = timezone.now()
        sent_count = 0
        failed_count = 0

        # Devis envoyés mais non consultés depuis 3 jours
        three_days_ago = now - timedelta(days=3)
        not_viewed = Quote.objects.filter(
            status='sent',
            updated_at__lte=three_days_ago,
            valid_until__gte=now.date(),
        )

        for quote in not_viewed:
            if _send_reminder_email(quote, reminder_type='not_viewed'):
                sent_count += 1
            else:
                failed_count += 1

        # Devis consultés mais non acceptés depuis 5 jours
        five_days_ago = now - timedelta(days=5)
        not_accepted = Quote.objects.filter(
            status='viewed',
            viewed_at__lte=five_days_ago,
            valid_until__gte=now.date(),
        )

        for quote in not_accepted:
            if _send_reminder_email(quote, reminder_type='not_accepted'):
                sent_count += 1
            else:
                failed_count += 1

        logger.info(f'send_quote_reminders: {sent_count} envoyés, {failed_count} échoués')
        return {'sent': sent_count, 'failed': failed_count}

    except Exception as exc:
        logger.error(f'send_quote_reminders error: {exc}')
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def send_lead_follow_ups(self):
    """
    Relance les leads chauds (score >= 50) qui n'ont pas de devis associé
    et qui ont été créés il y a plus de 48h.
    Cron recommandé : chaque jour à 10:00.
    """
    from leads.models import Lead
    from django.core.mail import send_mail
    from django.conf import settings

    try:
        cutoff = timezone.now() - timedelta(hours=48)
        hot_leads = Lead.objects.filter(
            score__gte=50,
            is_converted=False,
            quotes__isnull=True,
            created_at__lte=cutoff,
        )

        count = 0
        for lead in hot_leads:
            try:
                send_mail(
                    subject=f'Votre projet {lead.project_type.name if lead.project_type else "web"} — Suite de notre échange',
                    message=(
                        f'Bonjour {lead.name or ""},\n\n'
                        f'Je me permets de revenir vers vous suite à votre demande.\n'
                        f'Avez-vous eu le temps de réfléchir à votre projet ?\n\n'
                        f'Je serais ravi de vous préparer un devis personnalisé et gratuit.\n\n'
                        f'Obtenez votre devis : https://zsdevweb.fr/devis\n\n'
                        f'Cordialement,\nZsdevweb'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[lead.email],
                    fail_silently=True,
                )
                count += 1
            except Exception as e:
                logger.warning(f'Échec relance lead {lead.email}: {e}')

        logger.info(f'send_lead_follow_ups: {count} relances envoyées')
        return {'sent': count}

    except Exception as exc:
        logger.error(f'send_lead_follow_ups error: {exc}')
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def notify_admin_quote_signed(self, quote_id: int, accepted: bool, reason: str = '') -> str:
    """
    Notifie l'admin par email quand un devis est signé (accepté ou refusé).
    Appelé depuis QuoteSignView après la mise à jour du statut.
    """
    from .models import Quote
    from django.core.mail import send_mail
    from django.conf import settings

    try:
        quote = Quote.objects.get(pk=quote_id)
    except Quote.DoesNotExist:
        logger.error('notify_admin_quote_signed: Quote %s introuvable', quote_id)
        return 'not_found'

    action_str = 'ACCEPTÉ ✅' if accepted else 'REFUSÉ ❌'
    subject = f'Devis {quote.quote_number} {action_str} — {quote.client_name}'
    body = (
        f'Devis {quote.quote_number}\n'
        f'Client : {quote.client_name} ({quote.client_email})\n'
        f'Montant : {quote.total_ttc} € TTC\n'
        f'Statut : {action_str}\n'
    )
    if reason:
        body += f'Raison du refus : {reason}\n'

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        return f'sent:{quote.quote_number}'
    except Exception as exc:
        logger.error('notify_admin_quote_signed error: %s', exc)
        raise self.retry(exc=exc)


@shared_task
def cleanup_draft_quotes():
    """
    Supprime les devis en brouillon créés il y a plus de 30 jours sans activité.
    Cron recommandé : chaque lundi à 03:00.
    """
    from .models import Quote

    cutoff = timezone.now() - timedelta(days=30)
    deleted, _ = Quote.objects.filter(
        status='draft',
        updated_at__lte=cutoff,
    ).delete()

    logger.info(f'cleanup_draft_quotes: {deleted} brouillons supprimés')
    return {'deleted': deleted}


@shared_task(bind=True, max_retries=2)
def generate_and_send_quote(self, quote_id: int):
    """
    Génère le PDF et envoie le devis par email.
    Appelé après la création d'un devis via le wizard.
    """
    from .models import Quote
    from services.pdf_service import PdfService
    from services.email_service import EmailService

    try:
        quote = Quote.objects.get(pk=quote_id)

        # 1. Générer le PDF
        pdf_ok = PdfService.generate_quote_pdf(quote)
        if not pdf_ok:
            logger.warning(f'PDF non généré pour devis {quote.quote_number}')

        # 2. Envoyer l'email
        email_ok = EmailService.send_quote_to_client(quote)
        if not email_ok:
            logger.error(f'Échec envoi email devis {quote.quote_number}')

        return {'pdf': pdf_ok, 'email': email_ok}

    except Quote.DoesNotExist:
        logger.error(f'generate_and_send_quote: Quote {quote_id} introuvable')
        return {'error': 'not_found'}
    except Exception as exc:
        logger.error(f'generate_and_send_quote error: {exc}')
        raise self.retry(exc=exc)


# ---- Helper privé ----

def _send_reminder_email(quote, reminder_type: str) -> bool:
    """Envoie un email de rappel pour un devis."""
    from django.core.mail import send_mail
    from django.conf import settings

    try:
        if reminder_type == 'not_viewed':
            subject = f'Rappel : votre devis {quote.quote_number} vous attend'
            message = (
                f'Bonjour {quote.client_name},\n\n'
                f'Je reviens vers vous concernant votre devis {quote.quote_number} '
                f'pour un montant de {quote.total_ttc} € TTC.\n\n'
                f'Consultez votre devis : https://zsdevweb.fr/devis/{quote.uuid}\n\n'
                f'Ce devis est valable jusqu\'au {quote.valid_until}.\n\n'
                f'Cordialement,\nZsdevweb'
            )
        else:  # not_accepted
            subject = f'Des questions sur votre devis {quote.quote_number} ?'
            message = (
                f'Bonjour {quote.client_name},\n\n'
                f'Avez-vous eu l\'occasion d\'examiner votre devis {quote.quote_number} '
                f'({quote.total_ttc} € TTC) ?\n\n'
                f'Je suis disponible pour répondre à toutes vos questions.\n\n'
                f'Consulter / Accepter : https://zsdevweb.fr/devis/{quote.uuid}\n\n'
                f'Cordialement,\nZsdevweb'
            )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[quote.client_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f'Reminder email failed for {quote.quote_number}: {e}')
        return False
