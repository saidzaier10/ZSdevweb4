from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def notify_client_project_update(self, update_id: int) -> str:
    """
    Envoie un email au client quand une mise à jour visible est créée sur son projet.
    Retry automatique jusqu'à 3 fois en cas d'erreur SMTP.
    """
    from .models import ProjectUpdate

    try:
        update = (
            ProjectUpdate.objects
            .select_related('project__client')
            .get(pk=update_id, is_visible_to_client=True)
        )
    except ProjectUpdate.DoesNotExist:
        return f'Update {update_id} introuvable ou non visible — ignoré.'

    project = update.project
    client = project.client
    client_email = client.email
    client_name = client.get_full_name() or client.email

    frontend_url = getattr(settings, 'FRONTEND_URL', '')
    portal_url = f'{frontend_url}/espace-client/projets/{project.uuid}'

    context = {
        'update': update,
        'project': project,
        'client_name': client_name,
        'portal_url': portal_url,
        'frontend_url': frontend_url,
    }

    subject = f'[Zsdevweb] Mise à jour : {project.title}'
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@zsdevweb.fr')

    try:
        text_body = render_to_string('emails/project_update_notification.txt', context)
        html_body = render_to_string('emails/project_update_notification.html', context)

        msg = EmailMultiAlternatives(subject, text_body, from_email, [client_email])
        msg.attach_alternative(html_body, 'text/html')
        msg.send()

        return f'Email envoyé à {client_email} pour update {update_id}.'

    except Exception as exc:
        raise self.retry(exc=exc)
