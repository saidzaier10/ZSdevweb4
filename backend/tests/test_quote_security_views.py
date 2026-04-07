from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache
from rest_framework.test import APIClient

from quotes.models import Quote


class TestQuoteSecurityViews:
    def setup_method(self):
        cache.clear()
        self.client = APIClient()
        self.quote = Quote.objects.create(
            client_name='Client Test',
            client_email='client@example.com',
            signature_token='secure-signature-token',
        )

    def test_quote_pdf_requires_token_or_auth(self):
        url = reverse('quote-pdf', kwargs={'uuid': self.quote.uuid})

        response = self.client.get(url)

        assert response.status_code == 403

    def test_quote_sign_get_rejects_invalid_token(self):
        url = reverse('quote-sign', kwargs={'uuid': self.quote.uuid})

        response = self.client.get(url, {'token': 'invalid-token'})

        assert response.status_code == 400
        assert response.data['valid'] is False

    def test_quote_sign_post_rejects_invalid_token(self):
        url = reverse('quote-sign', kwargs={'uuid': self.quote.uuid})

        response = self.client.post(
            url,
            {'token': 'invalid-token', 'action': 'accept'},
            format='json',
        )

        assert response.status_code == 400

    def test_quote_pdf_allows_authenticated_user_without_token(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='StrongPassword123!'
        )
        self.client.force_authenticate(user=user)

        url = reverse('quote-pdf', kwargs={'uuid': self.quote.uuid})
        response = self.client.get(url)

        # Auth bypasses token check. If PDF does not yet exist, endpoint may return 503.
        assert response.status_code in (200, 503)

    def test_quote_sign_get_rate_limited_after_threshold(self):
        url = reverse('quote-sign', kwargs={'uuid': self.quote.uuid})

        for _ in range(10):
            response = self.client.get(url, {'token': 'invalid-token'})
            assert response.status_code == 400

        throttled = self.client.get(url, {'token': 'invalid-token'})
        assert throttled.status_code == 429
        assert throttled.data['detail'] == 'Trop de requetes. Reessayez plus tard.'
