import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from quotes.models import Quote
from quotes.permissions import IsOwnerOrStaffOrValidToken
from quotes.serializers import QuoteCreateSerializer, QuoteDetailSerializer
from services.quote_service import QuoteService
from services.pdf_service import PdfService
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

        quote = QuoteService().create_from_wizard(serializer.validated_data)

        try:
            from quotes.tasks import generate_and_send_quote
            generate_and_send_quote.delay(quote.pk)
        except Exception:
            PdfService.generate_quote_pdf(quote)

        return Response(QuoteDetailSerializer(quote).data, status=status.HTTP_201_CREATED)


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
        if instance.status == 'sent':
            instance.status = 'viewed'
            instance.viewed_at = timezone.now()
            instance.save(update_fields=['status', 'viewed_at'])
        data = self.get_serializer(instance).data
        data['recommendations'] = RecommendationService.get_recommendations_for_quote(instance)
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

        from services.email_service import EmailService
        success = EmailService.send_quote_to_client(quote)
        if success:
            return Response({'detail': 'Devis envoyé avec succès.'})
        return Response(
            {'detail': 'Erreur lors de l\'envoi. Consultez les logs.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
