from rest_framework import generics, permissions
from .models import FAQItem
from .serializers import FAQItemSerializer


class FAQListView(generics.ListAPIView):
    serializer_class = FAQItemSerializer
    permission_classes = [permissions.AllowAny]
    queryset = FAQItem.objects.filter(is_active=True)
