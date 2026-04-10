import secrets
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from django.utils import timezone
from django.utils.crypto import constant_time_compare
from django.http import FileResponse

from .models import Quote
from .permissions import IsOwnerOrStaffOrValidToken
from .serializers import QuoteCreateSerializer, QuoteDetailSerializer, PricePreviewSerializer
from services.quote_service import QuoteService
from services.pdf_service import PdfService
from services.email_service import EmailService
from services.recommendation_service import RecommendationService


class QuoteCreateView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'quote_create'

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

    def get(self, request, uuid):
        from django.utils.crypto import constant_time_compare
        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'detail': 'Devis non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        token = request.query_params.get('token', '')
        token_valid = token and quote.signature_token and constant_time_compare(str(token), str(quote.signature_token))
        if not token_valid and not (request.user.is_authenticated and request.user.is_staff):
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

    def get(self, request, uuid):
        """Vérifie la validité du token de signature."""
        token = request.query_params.get('token', '')
        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'valid': False, 'detail': 'Devis non trouvé.'}, status=404)

        if not token or not constant_time_compare(str(token), str(quote.signature_token)):
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
        if not token or not constant_time_compare(str(token), str(quote.signature_token)):
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

            # Notification admin
            _notify_admin_signature(quote, accepted=True)

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

            _notify_admin_signature(quote, accepted=False, reason=reason)

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

def _notify_admin_signature(quote, accepted: bool, reason: str = '') -> None:
    """Notifie l'admin par email lors d'une signature."""
    from django.core.mail import send_mail
    from django.conf import settings

    action_str = 'ACCEPTÉ ✅' if accepted else 'REFUSÉ ❌'
    subject = f'Devis {quote.quote_number} {action_str} — {quote.client_name}'
    body = (
        f'Devis {quote.quote_number}\n'
        f'Client : {quote.client_name} ({quote.client_email})\n'
        f'Montant : {quote.total_ttc} € TTC\n'
        f'Statut : {action_str}\n'
    )
    if reason:
        body += f'Raison du refus : {reason}\n'

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass
