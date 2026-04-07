from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .serializers import LeadCaptureSerializer
from services.lead_service import LeadService


class LeadCaptureView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key='ip', rate='20/m', method='POST', block=True))
    def post(self, request):
        serializer = LeadCaptureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = LeadService()
        lead, created = service.capture(**serializer.validated_data)

        return Response({
            'id': lead.pk,
            'email': lead.email,
            'score': lead.score,
            'created': created,
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
