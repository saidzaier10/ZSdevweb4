import logging
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from quotes.models import Quote
from ._helpers import is_token_valid

logger = logging.getLogger(__name__)


class QuoteSignView(APIView):
    """
    Signature électronique d'un devis via token unique.
    GET  → vérifie le token
    POST → accepte ou refuse le devis
    """
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='ip', rate='10/m', method='GET', block=True))
    def get(self, request, uuid):
        token = request.query_params.get('token', '')
        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'valid': False, 'detail': 'Devis non trouvé.'}, status=404)

        if not is_token_valid(token, quote.signature_token):
            logger.warning('quote_sign_get_invalid_token quote=%s ip=%s', quote.uuid, request.META.get('REMOTE_ADDR'))
            return Response({'valid': False, 'detail': 'Token invalide.'}, status=400)

        if quote.status in ('accepted', 'rejected', 'expired'):
            return Response({
                'valid': False,
                'detail': f'Ce devis est déjà {quote.get_status_display().lower()}.',
                'status': quote.status,
            }, status=400)

        return Response({
            'valid': True,
            'quote_number': quote.quote_number,
            'client_name': quote.client_name,
            'total_ttc': str(quote.total_ttc),
            'valid_until': quote.valid_until,
            'status': quote.status,
        })

    @method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True))
    def post(self, request, uuid):
        token = request.data.get('token', '')
        action = request.data.get('action', 'accept')

        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'detail': 'Devis non trouvé.'}, status=404)

        if not is_token_valid(token, quote.signature_token):
            logger.warning('quote_sign_post_invalid_token quote=%s ip=%s', quote.uuid, request.META.get('REMOTE_ADDR'))
            return Response({'detail': 'Token de signature invalide.'}, status=400)

        if quote.status in ('accepted', 'rejected'):
            return Response({'detail': f'Ce devis a déjà été {quote.get_status_display().lower()}.'}, status=400)

        if quote.status == 'expired':
            return Response({'detail': 'Ce devis a expiré.'}, status=400)

        now = timezone.now()

        if action == 'accept':
            return self._accept(request, quote, now)
        if action == 'reject':
            return self._reject(request, quote, now)
        return Response({'detail': 'Action invalide. Utilisez "accept" ou "reject".'}, status=400)

    # ── helpers privés ──

    def _accept(self, request, quote, now):
        signature_name = request.data.get('signature_name', '')
        quote.status = 'accepted'
        quote.signed_at = now
        if signature_name:
            quote.notes_internal += f'\nSigné par: {signature_name} le {now.strftime("%d/%m/%Y %H:%M")}'
        quote.save(update_fields=['status', 'signed_at', 'notes_internal'])

        if quote.lead:
            from leads.models import Lead
            Lead.objects.filter(pk=quote.lead_id).update(is_converted=True, converted_at=now)

        from quotes.tasks import notify_admin_quote_signed
        notify_admin_quote_signed.delay(quote.pk, accepted=True)
        logger.info('quote_signed_accepted quote=%s ip=%s', quote.uuid, request.META.get('REMOTE_ADDR'))

        return Response({
            'detail': 'Devis accepté avec succès. Nous vous contacterons sous 24h.',
            'status': 'accepted',
            'signed_at': now.isoformat(),
        })

    def _reject(self, request, quote, now):
        reason = request.data.get('reason', '')
        quote.status = 'rejected'
        if reason:
            quote.notes_internal += f'\nRefusé le {now.strftime("%d/%m/%Y")}. Raison: {reason}'
        quote.save(update_fields=['status', 'notes_internal'])

        from quotes.tasks import notify_admin_quote_signed
        notify_admin_quote_signed.delay(quote.pk, accepted=False, reason=reason)
        logger.info('quote_signed_rejected quote=%s ip=%s', quote.uuid, request.META.get('REMOTE_ADDR'))

        return Response({'detail': 'Devis refusé. Merci de nous avoir contactés.', 'status': 'rejected'})
