from unittest.mock import patch

from django.test import Client
from django.urls import reverse


class TestHealthEndpoint:
    def setup_method(self):
        self.client = Client()

    def test_health_ok_when_db_and_cache_are_available(self):
        response = self.client.get(reverse('health'))

        assert response.status_code == 200
        body = response.json()
        assert body['status'] == 'ok'
        assert body['mode'] == 'readiness'
        assert body['checks']['database']['ok'] is True
        assert body['checks']['cache']['ok'] is True

    def test_liveness_always_returns_ok(self):
        response = self.client.get(reverse('health-liveness'))

        assert response.status_code == 200
        assert response.json()['status'] == 'ok'
        assert response.json()['mode'] == 'liveness'

    def test_readiness_uses_dependency_checks(self):
        response = self.client.get(reverse('health-readiness'))

        assert response.status_code == 200
        assert response.json()['mode'] == 'readiness'

    @patch('zsdevweb.urls.connection')
    def test_health_degraded_when_db_check_fails(self, mocked_connection):
        mocked_connection.cursor.side_effect = RuntimeError('db down')

        response = self.client.get(reverse('health'))

        assert response.status_code == 503
        body = response.json()
        assert body['status'] == 'degraded'
        assert body['mode'] == 'readiness'
        assert body['checks']['database']['ok'] is False

    @patch('zsdevweb.urls.cache')
    def test_health_degraded_when_cache_check_fails(self, mocked_cache):
        mocked_cache.set.side_effect = RuntimeError('cache down')

        response = self.client.get(reverse('health'))

        assert response.status_code == 503
        body = response.json()
        assert body['status'] == 'degraded'
        assert body['mode'] == 'readiness'
        assert body['checks']['cache']['ok'] is False

    @patch('zsdevweb.urls.cache')
    def test_health_degraded_when_cache_get_mismatch(self, mocked_cache):
        mocked_cache.get.return_value = 'unexpected'

        response = self.client.get(reverse('health-readiness'))

        assert response.status_code == 503
        body = response.json()
        assert body['status'] == 'degraded'
        assert body['mode'] == 'readiness'
        assert body['checks']['cache']['ok'] is False
