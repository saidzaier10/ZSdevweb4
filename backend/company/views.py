from rest_framework import generics, permissions
from .models import CompanySettings
from .serializers import CompanySettingsSerializer


class CompanySettingsView(generics.RetrieveAPIView):
    serializer_class = CompanySettingsSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return CompanySettings.get()
