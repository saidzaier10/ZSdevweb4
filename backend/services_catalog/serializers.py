from rest_framework import serializers
from .models import ProjectCategory, ProjectType, DesignOption, ComplexityLevel, SupplementaryOption


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ('id', 'name', 'slug', 'description', 'base_price', 'min_days', 'max_days')


class ProjectCategorySerializer(serializers.ModelSerializer):
    project_types = ProjectTypeSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectCategory
        fields = ('id', 'name', 'slug', 'description', 'icon', 'project_types')


class DesignOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignOption
        fields = ('id', 'name', 'slug', 'description', 'price_supplement')


class ComplexityLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexityLevel
        fields = ('id', 'name', 'slug', 'description', 'multiplier')


class SupplementaryOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplementaryOption
        fields = ('id', 'name', 'slug', 'description', 'price', 'is_recurring')
