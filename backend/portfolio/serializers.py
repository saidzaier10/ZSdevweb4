import os

from rest_framework import serializers

from .models import PortfolioProject, Testimonial


def _webp_url(request, image_field):
    """Retourne l'URL du fichier .webp s'il existe, sinon None."""
    if not image_field:
        return None
    try:
        webp_path = os.path.splitext(image_field.path)[0] + '.webp'
        if os.path.exists(webp_path):
            original_url = request.build_absolute_uri(image_field.url) if request else image_field.url
            return os.path.splitext(original_url)[0] + '.webp'
    except (ValueError, AttributeError):
        pass
    return None


class PortfolioProjectSerializer(serializers.ModelSerializer):
    image_webp = serializers.SerializerMethodField()

    def get_image_webp(self, obj):
        return _webp_url(self.context.get('request'), obj.image)

    class Meta:
        model = PortfolioProject
        fields = ('id', 'title', 'slug', 'tagline', 'description',
                  'tech_stack', 'image', 'image_webp', 'url', 'github_url',
                  'client_name', 'is_featured', 'order')


class TestimonialSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Testimonial
        fields = ('id', 'client_name', 'client_company', 'client_role',
                  'client_avatar', 'content', 'rating', 'project_title', 'is_featured')


class PortfolioProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour la page projet individuelle."""
    testimonials = TestimonialSerializer(many=True, read_only=True)
    image_webp = serializers.SerializerMethodField()
    image_secondary_webp = serializers.SerializerMethodField()

    def get_image_webp(self, obj):
        return _webp_url(self.context.get('request'), obj.image)

    def get_image_secondary_webp(self, obj):
        return _webp_url(self.context.get('request'), obj.image_secondary)

    class Meta:
        model = PortfolioProject
        fields = ('id', 'title', 'slug', 'tagline', 'description',
                  'tech_stack', 'image', 'image_webp', 'image_secondary',
                  'image_secondary_webp', 'url', 'github_url',
                  'client_name', 'is_featured', 'order', 'created_at', 'testimonials')
