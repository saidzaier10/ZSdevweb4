"""
Configuration globale pytest.
Active CELERY_TASK_ALWAYS_EAGER pour exécuter les tâches de façon synchrone sans worker.
"""
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


@pytest.fixture(autouse=True)
def use_dummy_cache(settings):
    """Utilise le cache mémoire en test pour éviter la dépendance Redis."""
    settings.CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }


@pytest.fixture(autouse=True)
def disable_throttling(request, settings):
    """
    Désactive tout rate limiting en test sauf pour les tests marqués @pytest.mark.with_throttling.

    - RATELIMIT_ENABLE=False      : désactive django_ratelimit (@ratelimit decorator)
    - mock ScopedRateThrottle     : bypass fiable du throttle DRF (évite les 429 entre tests)

    Les tests qui vérifient le comportement du rate limiting doivent être marqués
    @pytest.mark.with_throttling — ils ne passent pas par ce bypass.
    """
    if request.node.get_closest_marker('with_throttling'):
        yield
        return

    settings.RATELIMIT_ENABLE = False
    from unittest.mock import patch
    with patch('rest_framework.throttling.ScopedRateThrottle.allow_request', return_value=True):
        yield
