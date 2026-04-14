from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from quotes.serializers import PricePreviewSerializer
from services.quote_service import QuoteService


class PricePreviewView(APIView):
    """Calcul de prix stateless — aucune persistance en DB."""
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='ip', rate='30/m', method='POST', block=True))
    def post(self, request):
        serializer = PricePreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pricing = QuoteService().calculate_price_preview(serializer.validated_data)
            return Response({k: str(v) for k, v in pricing.items()})
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
