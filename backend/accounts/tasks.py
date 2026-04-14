from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email(self, user_id: int, reset_url: str) -> str:
    """
    Envoie le lien de réinitialisation de mot de passe.
    Appelé depuis PasswordResetRequestView pour ne pas bloquer le thread HTTP.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f'User {user_id} introuvable — ignoré.'

    context = {
        'user': user,
        'reset_url': reset_url,
        'frontend_url': settings.FRONTEND_URL,
    }
    subject = '[Zsdevweb] Réinitialisation de votre mot de passe'

    try:
        text_body = render_to_string('emails/password_reset.txt', context)
        html_body = render_to_string('emails/password_reset.html', context)

        msg = EmailMultiAlternatives(
            subject, text_body, settings.DEFAULT_FROM_EMAIL, [user.email]
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()

        return f'Email de reset envoyé à {user.email}.'

    except Exception as exc:
        raise self.retry(exc=exc)
