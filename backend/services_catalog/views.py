from rest_framework import generics, permissions
from django.db.models import Prefetch
from .models import ProjectCategory, ProjectType, DesignOption, ComplexityLevel, SupplementaryOption
from .serializers import (
    ProjectCategorySerializer,
    ProjectTypeSerializer,
    DesignOptionSerializer,
    ComplexityLevelSerializer,
    SupplementaryOptionSerializer,
)


class ProjectCategoryListView(generics.ListAPIView):
    serializer_class = ProjectCategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = ProjectCategory.objects.filter(is_active=True).prefetch_related(
        Prefetch('project_types', queryset=ProjectType.objects.filter(is_active=True))
    )


class ProjectTypeListView(generics.ListAPIView):
    serializer_class = ProjectTypeSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ProjectType.objects.filter(is_active=True).select_related('category')


class DesignOptionListView(generics.ListAPIView):
    serializer_class = DesignOptionSerializer
    permission_classes = [permissions.AllowAny]
    queryset = DesignOption.objects.filter(is_active=True)


class ComplexityLevelListView(generics.ListAPIView):
    serializer_class = ComplexityLevelSerializer
    permission_classes = [permissions.AllowAny]
    queryset = ComplexityLevel.objects.all()


class SupplementaryOptionListView(generics.ListAPIView):
    serializer_class = SupplementaryOptionSerializer
    permission_classes = [permissions.AllowAny]
    queryset = SupplementaryOption.objects.filter(is_active=True)
