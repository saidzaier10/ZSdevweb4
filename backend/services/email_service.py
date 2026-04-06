"""
EmailService — Envoi d'emails (devis, contact, notifications).
"""
import logging
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def _send_admin_notification(subject: str, body: str) -> None:
        """Méthode générique pour notifier l'admin. DRY — évite la duplication."""
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f'Erreur notification admin ({subject}): {e}')

    @staticmethod
    def send_quote_to_client(quote) -> bool:
        """
        Envoie le devis par email au client.
        Crée un QuoteEmailLog.
        Retourne True si succès.
        """
        from quotes.models import QuoteEmailLog

        subject = f'Votre devis {quote.quote_number} — Zsdevweb'

        frontend_url = getattr(settings, 'FRONTEND_URL', 'https://zsdevweb.fr')
        context = {
            'quote': quote,
            'company_name': 'Zsdevweb',
            'view_url': f'{frontend_url}/devis/{quote.uuid}',
            'sign_url': f'{frontend_url}/devis/{quote.uuid}/signer?token={quote.signature_token}',
        }

        try:
            html_content = render_to_string('emails/quote_to_client.html', context)
            text_content = render_to_string('emails/quote_to_client.txt', context)
        except Exception as e:
            # Fallback si templates non trouvés
            html_content = f"""
            <h2>Votre devis {quote.quote_number}</h2>
            <p>Bonjour {quote.client_name},</p>
            <p>Voici votre devis pour un montant de <strong>{quote.total_ttc}€ TTC</strong>.</p>
            <p>Ce devis est valable jusqu'au {quote.valid_until}.</p>
            <p>Cordialement,<br>Zsdevweb</p>
            """
            text_content = f"Devis {quote.quote_number} — Total TTC: {quote.total_ttc}€"

        log = QuoteEmailLog(
            quote=quote,
            sent_to=quote.client_email,
            subject=subject,
        )

        try:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[quote.client_email],
            )
            msg.attach_alternative(html_content, 'text/html')

            if quote.pdf_file:
                with open(quote.pdf_file.path, 'rb') as f:
                    msg.attach(
                        filename=f'Devis_{quote.quote_number}.pdf',
                        content=f.read(),
                        mimetype='application/pdf'
                    )

            msg.send()

            log.status = QuoteEmailLog.STATUS_SENT
            log.save()

            # Mettre à jour le statut du devis
            quote.status = 'sent'
            quote.save(update_fields=['status'])

            return True

        except Exception as e:
            logger.error(f'Erreur envoi email devis {quote.quote_number}: {e}')
            log.status = QuoteEmailLog.STATUS_FAILED
            log.error_message = str(e)
            log.save()
            return False

    @classmethod
    def send_contact_notification(cls, contact_request) -> None:
        """Notifie l'admin d'une nouvelle demande de contact."""
        subject = f'Nouveau contact: {contact_request.name} — {contact_request.get_subject_display()}'
        body = (
            f"Nom: {contact_request.name}\n"
            f"Email: {contact_request.email}\n"
            f"Téléphone: {contact_request.phone or 'Non renseigné'}\n"
            f"Sujet: {contact_request.get_subject_display()}\n\n"
            f"Message:\n{contact_request.message}"
        )
        cls._send_admin_notification(subject, body)

    @classmethod
    def send_audit_notification(cls, audit_request) -> None:
        """Notifie l'admin d'une nouvelle demande d'audit."""
        subject = f"Nouvelle demande d'audit: {audit_request.site_url}"
        body = (
            f"Nom: {audit_request.name}\n"
            f"Email: {audit_request.email}\n"
            f"Site: {audit_request.site_url}\n"
            f"Problèmes: {audit_request.current_issues or 'Non renseigné'}\n"
            f"Budget: {audit_request.budget_range or 'Non renseigné'}"
        )
        cls._send_admin_notification(subject, body)
