from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ClientProject
from .serializers import ClientProjectSerializer, ClientProjectListSerializer


class ClientProjectListView(generics.ListAPIView):
    """Liste des projets du client connecté."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientProjectListSerializer

    def get_queryset(self):
        return ClientProject.objects.filter(
            client=self.request.user
        ).prefetch_related('updates', 'documents')


class ClientProjectDetailView(generics.RetrieveAPIView):
    """Détail d'un projet (avec mises à jour et documents)."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientProjectSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        return ClientProject.objects.filter(
            client=self.request.user
        ).prefetch_related('documents')

    def get_object(self):
        obj = super().get_object()
        # Injecter uniquement les updates visibles par le client
        obj.updates_visible = obj.updates.filter(is_visible_to_client=True)
        return obj
