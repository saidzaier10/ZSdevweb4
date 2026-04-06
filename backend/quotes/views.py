from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from .models import Quote
from .serializers import QuoteCreateSerializer, QuoteDetailSerializer, PricePreviewSerializer
from services.quote_service import QuoteService
from services.pdf_service import PdfService
from services.email_service import EmailService
from services.recommendation_service import RecommendationService


class QuoteCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = QuoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = QuoteService()
        quote = service.create_from_wizard(serializer.validated_data)

        # Générer le PDF en arrière-plan (best effort)
        PdfService.generate_quote_pdf(quote)

        return Response(
            QuoteDetailSerializer(quote).data,
            status=status.HTTP_201_CREATED
        )


class QuoteDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = QuoteDetailSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return Quote.objects.select_related(
            'project_type', 'design_option', 'complexity'
        ).prefetch_related('options')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Marquer comme "vu"
        if instance.status == Quote.STATUS_SENT:
            instance.status = Quote.STATUS_VIEWED
            instance.viewed_at = timezone.now()
            instance.save(update_fields=['status', 'viewed_at'])

        serializer = self.get_serializer(instance)
        data = serializer.data

        # Ajouter les recommandations
        recommendations = RecommendationService.get_recommendations_for_quote(instance)
        data['recommendations'] = recommendations

        return Response(data)


class QuoteSendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, uuid):
        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'detail': 'Devis non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        # Générer le PDF si pas encore fait
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
        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'detail': 'Devis non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

        if not quote.pdf_file:
            PdfService.generate_quote_pdf(quote)

        if not quote.pdf_file:
            return Response(
                {'detail': 'PDF non disponible.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        from django.http import FileResponse
        return FileResponse(
            quote.pdf_file.open('rb'),
            content_type='application/pdf',
            as_attachment=True,
            filename=f'Devis_{quote.quote_number}.pdf',
        )


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
            # Convertir les Decimal en str pour JSON
            return Response({k: str(v) for k, v in pricing.items()})
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
