from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import ContactRequest
from .serializers import ContactRequestSerializer
from services.email_service import EmailService
from services.lead_service import LeadService


class ContactRequestCreateView(generics.CreateAPIView):
    serializer_class = ContactRequestSerializer
    permission_classes = [permissions.AllowAny]

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
