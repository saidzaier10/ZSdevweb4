"""
Tests des tâches Celery — exécutées en mode synchrone (CELERY_TASK_ALWAYS_EAGER=True).
"""
import pytest
from datetime import timedelta
from unittest.mock import patch, MagicMock

from django.utils import timezone
from django.core import mail

from quotes.models import Quote
from quotes.tasks import (
    expire_old_quotes,
    cleanup_draft_quotes,
    generate_and_send_quote,
    send_lead_follow_ups,
)
from .factories import QuoteFactory, UserFactory


# ─────────────────────────────────────────────
# expire_old_quotes
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestExpireOldQuotes:
    def _past_date(self, days=1):
        return (timezone.now() - timedelta(days=days)).date()

    def _future_date(self, days=30):
        return (timezone.now() + timedelta(days=days)).date()

    def test_expires_overdue_sent_quotes(self):
        q = QuoteFactory(status=Quote.STATUS_SENT, valid_until=self._past_date(2))
        result = expire_old_quotes.delay()
        q.refresh_from_db()
        assert q.status == Quote.STATUS_EXPIRED
        assert result.result['expired'] == 1

    def test_expires_overdue_draft_quotes(self):
        q = QuoteFactory(status=Quote.STATUS_DRAFT, valid_until=self._past_date(5))
        expire_old_quotes.delay()
        q.refresh_from_db()
        assert q.status == Quote.STATUS_EXPIRED

    def test_does_not_expire_future_quotes(self):
        q = QuoteFactory(status=Quote.STATUS_SENT, valid_until=self._future_date(10))
        expire_old_quotes.delay()
        q.refresh_from_db()
        assert q.status == Quote.STATUS_SENT

    def test_does_not_touch_already_accepted(self):
        q = QuoteFactory(status=Quote.STATUS_ACCEPTED, valid_until=self._past_date(5))
        expire_old_quotes.delay()
        q.refresh_from_db()
        assert q.status == Quote.STATUS_ACCEPTED

    def test_returns_correct_count(self):
        QuoteFactory(status=Quote.STATUS_SENT, valid_until=self._past_date(1))
        QuoteFactory(status=Quote.STATUS_SENT, valid_until=self._past_date(2))
        QuoteFactory(status=Quote.STATUS_SENT, valid_until=self._future_date(5))
        result = expire_old_quotes.delay()
        assert result.result['expired'] == 2


# ─────────────────────────────────────────────
# cleanup_draft_quotes
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestCleanupDraftQuotes:
    def test_deletes_old_drafts(self):
        q = QuoteFactory(status=Quote.STATUS_DRAFT)
        # Simuler un devis vieux de 31 jours
        Quote.objects.filter(pk=q.pk).update(
            updated_at=timezone.now() - timedelta(days=31)
        )
        result = cleanup_draft_quotes.delay()
        assert result.result['deleted'] == 1
        assert not Quote.objects.filter(pk=q.pk).exists()

    def test_keeps_recent_drafts(self):
        q = QuoteFactory(status=Quote.STATUS_DRAFT)
        result = cleanup_draft_quotes.delay()
        assert result.result['deleted'] == 0
        assert Quote.objects.filter(pk=q.pk).exists()

    def test_does_not_delete_sent_old_quotes(self):
        q = QuoteFactory(status=Quote.STATUS_SENT)
        Quote.objects.filter(pk=q.pk).update(
            updated_at=timezone.now() - timedelta(days=35)
        )
        result = cleanup_draft_quotes.delay()
        assert result.result['deleted'] == 0
        assert Quote.objects.filter(pk=q.pk).exists()


# ─────────────────────────────────────────────
# generate_and_send_quote
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestGenerateAndSendQuote:
    @patch('services.pdf_service.PdfService.generate_quote_pdf', return_value=True)
    @patch('services.email_service.EmailService.send_quote_to_client', return_value=True)
    def test_success(self, mock_email, mock_pdf):
        q = QuoteFactory()
        result = generate_and_send_quote.delay(q.pk)
        assert result.result == {'pdf': True, 'email': True}
        mock_pdf.assert_called_once_with(q)
        mock_email.assert_called_once_with(q)

    @patch('services.pdf_service.PdfService.generate_quote_pdf', return_value=False)
    @patch('services.email_service.EmailService.send_quote_to_client', return_value=True)
    def test_pdf_failure_still_sends_email(self, mock_email, mock_pdf):
        q = QuoteFactory()
        result = generate_and_send_quote.delay(q.pk)
        assert result.result['pdf'] is False
        assert result.result['email'] is True

    def test_non_existent_quote_returns_error(self):
        result = generate_and_send_quote.delay(99999)
        assert result.result == {'error': 'not_found'}


# ─────────────────────────────────────────────
# send_lead_follow_ups
# ─────────────────────────────────────────────

@pytest.mark.django_db
class TestSendLeadFollowUps:
    def test_runs_without_leads(self):
        """La tâche doit terminer sans erreur même sans leads."""
        result = send_lead_follow_ups.delay()
        assert result.result['sent'] == 0

    def test_sends_email_for_hot_lead(self):
        """Un lead chaud (score >= 50) sans devis doit recevoir un email de relance."""
        from leads.models import Lead
        Lead.objects.create(
            email='hot@example.com',
            name='Lead Chaud',
            score=75,
            is_converted=False,
            created_at=timezone.now() - timedelta(hours=72),
        )
        result = send_lead_follow_ups.delay()
        assert result.result['sent'] == 1
        assert len(mail.outbox) == 1
        assert 'hot@example.com' in mail.outbox[0].to

    def test_does_not_send_for_cold_lead(self):
        """Un lead froid (score < 50) ne doit pas recevoir de relance."""
        from leads.models import Lead
        Lead.objects.create(
            email='cold@example.com',
            score=30,
            is_converted=False,
            created_at=timezone.now() - timedelta(hours=72),
        )
        result = send_lead_follow_ups.delay()
        assert result.result['sent'] == 0

    def test_does_not_send_for_recent_lead(self):
        """Un lead créé il y a moins de 48h ne doit pas encore être relancé."""
        from leads.models import Lead
        Lead.objects.create(
            email='recent@example.com',
            score=80,
            is_converted=False,
            created_at=timezone.now() - timedelta(hours=24),
        )
        result = send_lead_follow_ups.delay()
        assert result.result['sent'] == 0

    def test_does_not_send_for_converted_lead(self):
        """Un lead converti ne doit pas recevoir de relance."""
        from leads.models import Lead
        Lead.objects.create(
            email='converted@example.com',
            score=90,
            is_converted=True,
            created_at=timezone.now() - timedelta(hours=72),
        )
        result = send_lead_follow_ups.delay()
        assert result.result['sent'] == 0
