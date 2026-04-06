from rest_framework import generics, permissions
from .models import PortfolioProject, Testimonial
from .serializers import PortfolioProjectSerializer, TestimonialSerializer


class PortfolioProjectListView(generics.ListAPIView):
    serializer_class = PortfolioProjectSerializer
    permission_classes = [permissions.AllowAny]
    queryset = PortfolioProject.objects.filter(is_published=True)


class TestimonialListView(generics.ListAPIView):
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Testimonial.objects.filter(is_active=True)
