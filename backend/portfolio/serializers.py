from rest_framework import serializers
from .models import PortfolioProject, Testimonial


class PortfolioProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioProject
        fields = ('id', 'title', 'slug', 'tagline', 'description',
                  'tech_stack', 'image', 'url', 'github_url',
                  'client_name', 'is_featured', 'order')


class TestimonialSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Testimonial
        fields = ('id', 'client_name', 'client_company', 'client_role',
                  'client_avatar', 'content', 'rating', 'project_title', 'is_featured')
