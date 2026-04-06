from rest_framework import serializers
from .models import ClientProject, ProjectUpdate, ProjectDocument


class ProjectDocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectDocument
        fields = ('id', 'doc_type', 'name', 'file_url', 'description', 'uploaded_at')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectUpdate
        fields = ('id', 'update_type', 'title', 'content', 'created_at')


class ClientProjectSerializer(serializers.ModelSerializer):
    updates = ProjectUpdateSerializer(
        many=True, read_only=True, source='updates_visible'
    )
    documents = ProjectDocumentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    quote_number = serializers.CharField(source='quote.quote_number', read_only=True)
    quote_uuid = serializers.UUIDField(source='quote.uuid', read_only=True)

    class Meta:
        model = ClientProject
        fields = (
            'uuid', 'title', 'description',
            'status', 'status_display', 'progress_percent',
            'started_at', 'estimated_delivery', 'delivered_at',
            'site_url', 'repo_url',
            'quote_number', 'quote_uuid',
            'updates', 'documents',
            'created_at', 'updated_at',
        )


class ClientProjectListSerializer(serializers.ModelSerializer):
    """Version allégée pour la liste."""
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ClientProject
        fields = (
            'uuid', 'title', 'status', 'status_display',
            'progress_percent', 'estimated_delivery', 'updated_at',
        )
