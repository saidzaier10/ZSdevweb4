from rest_framework import generics, permissions
from .models import AuditRequest
from .serializers import AuditRequestSerializer
from services.email_service import EmailService
from services.lead_service import LeadService


class AuditRequestCreateView(generics.CreateAPIView):
    serializer_class = AuditRequestSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        instance = serializer.save()
        LeadService().capture(
            email=instance.email,
            source='audit_form',
            name=instance.name,
            phone=instance.phone,
            company=instance.company,
        )
        EmailService.send_audit_notification(instance)
