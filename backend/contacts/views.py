from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .models import ContactRequest
from .serializers import ContactRequestSerializer
from services.email_service import EmailService
from services.lead_service import LeadService


class ContactRequestCreateView(generics.CreateAPIView):
    serializer_class = ContactRequestSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'contact_create'

    @method_decorator(ratelimit(key='ip', rate='10/m', method='POST', block=True))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        # Capture lead
        LeadService().capture(
            email=instance.email,
            source='contact_form',
            name=instance.name,
            phone=instance.phone,
            company=instance.company,
        )
        # Notification admin
        EmailService.send_contact_notification(instance)
