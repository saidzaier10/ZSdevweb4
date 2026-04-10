from rest_framework import generics, permissions
from .models import PortfolioProject, Testimonial
from .serializers import PortfolioProjectSerializer, PortfolioProjectDetailSerializer, TestimonialSerializer


class PortfolioProjectListView(generics.ListAPIView):
    serializer_class = PortfolioProjectSerializer
    permission_classes = [permissions.AllowAny]
    queryset = PortfolioProject.objects.filter(is_published=True)


class PortfolioProjectDetailView(generics.RetrieveAPIView):
    """Vue détaillée d'un projet portfolio, accessible par slug."""
    serializer_class = PortfolioProjectDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = PortfolioProject.objects.filter(is_published=True)
    lookup_field = 'slug'


class TestimonialListView(generics.ListAPIView):
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Testimonial.objects.filter(is_active=True)
