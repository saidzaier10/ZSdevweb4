"""
Configuration globale pytest.
Active CELERY_TASK_ALWAYS_EAGER pour exécuter les tâches de façon synchrone sans worker.
"""
import django
import pytest


@pytest.fixture(autouse=True)
def celery_eager_mode(settings):
    """Force l'exécution synchrone des tâches Celery dans tous les tests."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True


@pytest.fixture(autouse=True)
def disable_email_sending(settings):
    """Remplace le backend email par locmem en test (pas de SMTP réel)."""
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
