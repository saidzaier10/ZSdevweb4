import secrets
import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from django.utils import timezone
from django.utils.crypto import constant_time_compare
from django.utils.decorators import method_decorator
from django.http import FileResponse
from django_ratelimit.decorators import ratelimit

from .models import Quote
from .permissions import IsOwnerOrStaffOrValidToken
from .serializers import QuoteCreateSerializer, QuoteDetailSerializer, PricePreviewSerializer
from services.quote_service import QuoteService
from services.pdf_service import PdfService
from services.email_service import EmailService
from services.recommendation_service import RecommendationService


logger = logging.getLogger(__name__)


class QuoteCreateView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'quote_create'

    @method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True))
    def post(self, request):
        serializer = QuoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = QuoteService()
        quote = service.create_from_wizard(serializer.validated_data)

        # Générer PDF + envoyer email en tâche async (best effort en sync si Celery indispo)
        try:
            from .tasks import generate_and_send_quote
            generate_and_send_quote.delay(quote.pk)
        except Exception:
            PdfService.generate_quote_pdf(quote)

        return Response(
            QuoteDetailSerializer(quote).data,
            status=status.HTTP_201_CREATED
        )


class QuoteDetailView(generics.RetrieveAPIView):
    permission_classes = [IsOwnerOrStaffOrValidToken]
    serializer_class = QuoteDetailSerializer
    lookup_field = 'uuid'

    @method_decorator(ratelimit(key='ip', rate='60/m', method='GET', block=True))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Quote.objects.select_related(
            'project_type', 'design_option', 'complexity'
        ).prefetch_related('options')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Marquer comme "vu"
        if instance.status == 'sent':
            instance.status = 'viewed'
            instance.viewed_at = timezone.now()
            instance.save(update_fields=['status', 'viewed_at'])

        serializer = self.get_serializer(instance)
        data = serializer.data

        # Ajouter les recommandations
        recommendations = RecommendationService.get_recommendations_for_quote(instance)
        data['recommendations'] = recommendations

        return Response(data)


class QuoteSendView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, uuid):
        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'detail': 'Devis non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        if not quote.pdf_file:
            PdfService.generate_quote_pdf(quote)

        success = EmailService.send_quote_to_client(quote)

        if success:
            return Response({'detail': 'Devis envoyé avec succès.'})
        return Response(
            {'detail': 'Erreur lors de l\'envoi. Consultez les logs.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class QuotePdfView(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='ip', rate='20/m', method='GET', block=True))
    def get(self, request, uuid):
        from django.utils.crypto import constant_time_compare
        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'detail': 'Devis non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        if not _is_token_valid(request.query_params.get('token', ''), quote.signature_token) and not request.user.is_authenticated:
            logger.warning('quote_pdf_access_denied quote=%s ip=%s', quote.uuid, request.META.get('REMOTE_ADDR'))
            return Response({'detail': 'Accès refusé.'}, status=status.HTTP_403_FORBIDDEN)

        if not quote.pdf_file:
            PdfService.generate_quote_pdf(quote)

        if not quote.pdf_file:
            return Response(
                {'detail': 'PDF non disponible.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        from django.conf import settings as django_settings
        if not django_settings.DEBUG:
            from django.http import HttpResponse
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Devis_{quote.quote_number}.pdf"'
            response['X-Accel-Redirect'] = f'/media/{quote.pdf_file.name}'
            return response

        return FileResponse(
            quote.pdf_file.open('rb'),
            content_type='application/pdf',
            as_attachment=True,
            filename=f'Devis_{quote.quote_number}.pdf',
        )


class QuoteSignView(APIView):
    """
    Signature électronique d'un devis via token unique.
    GET  /api/v1/quotes/{uuid}/sign/?token=xxx  → vérifie le token
    POST /api/v1/quotes/{uuid}/sign/            → signe le devis
    """
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='ip', rate='10/m', method='GET', block=True))
    def get(self, request, uuid):
        """Vérifie la validité du token de signature."""
        token = request.query_params.get('token', '')
        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'valid': False, 'detail': 'Devis non trouvé.'}, status=404)

        if not _is_token_valid(token, quote.signature_token):
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
        """
        Accepte ou refuse le devis.
        Body: { "token": "xxx", "action": "accept" | "reject", "signature_name": "..." }
        """
        token = request.data.get('token', '')
        action = request.data.get('action', 'accept')
        signature_name = request.data.get('signature_name', '')

        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'detail': 'Devis non trouvé.'}, status=404)

        # Valider le token
        if not _is_token_valid(token, quote.signature_token):
            logger.warning('quote_sign_post_invalid_token quote=%s ip=%s', quote.uuid, request.META.get('REMOTE_ADDR'))
            return Response({'detail': 'Token de signature invalide.'}, status=400)

        # Vérifier que le devis est signable
        if quote.status in ('accepted', 'rejected'):
            return Response({
                'detail': f'Ce devis a déjà été {quote.get_status_display().lower()}.',
            }, status=400)

        if quote.status == 'expired':
            return Response({'detail': 'Ce devis a expiré.'}, status=400)

        now = timezone.now()

        if action == 'accept':
            quote.status = 'accepted'
            quote.signed_at = now
            if signature_name:
                quote.notes_internal += f'\nSigné par: {signature_name} le {now.strftime("%d/%m/%Y %H:%M")}'
            quote.save(update_fields=['status', 'signed_at', 'notes_internal'])

            # Mettre à jour le lead si existant
            if quote.lead:
                from django.db.models import F
                from leads.models import Lead
                Lead.objects.filter(pk=quote.lead_id).update(
                    is_converted=True,
                    converted_at=now,
                )

            # Notification admin (async)
            from .tasks import notify_admin_quote_signed
            notify_admin_quote_signed.delay(quote.pk, accepted=True)
            logger.info('quote_signed_accepted quote=%s ip=%s', quote.uuid, request.META.get('REMOTE_ADDR'))

            return Response({
                'detail': 'Devis accepté avec succès. Nous vous contacterons sous 24h.',
                'status': 'accepted',
                'signed_at': now.isoformat(),
            })

        elif action == 'reject':
            reason = request.data.get('reason', '')
            quote.status = 'rejected'
            if reason:
                quote.notes_internal += f'\nRefusé le {now.strftime("%d/%m/%Y")}. Raison: {reason}'
            quote.save(update_fields=['status', 'notes_internal'])

            from .tasks import notify_admin_quote_signed
            notify_admin_quote_signed.delay(quote.pk, accepted=False, reason=reason)
            logger.info('quote_signed_rejected quote=%s ip=%s', quote.uuid, request.META.get('REMOTE_ADDR'))

            return Response({
                'detail': 'Devis refusé. Merci de nous avoir contactés.',
                'status': 'rejected',
            })

        return Response({'detail': 'Action invalide. Utilisez "accept" ou "reject".'}, status=400)


class PricePreviewView(APIView):
    """
    Endpoint stateless pour le calcul de prix en temps réel.
    Aucune persistance en DB.
    """
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='ip', rate='30/m', method='POST', block=True))
    def post(self, request):
        serializer = PricePreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = QuoteService()
        try:
            pricing = service.calculate_price_preview(serializer.validated_data)
            return Response({k: str(v) for k, v in pricing.items()})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ---- Helpers ----

def _is_token_valid(provided_token: str, expected_token: str) -> bool:
    """Compare les tokens de façon sûre et résiste aux attaques timing."""
    if not provided_token or not expected_token:
        return False
    return constant_time_compare(str(provided_token), str(expected_token))

