from rest_framework import serializers
from .models import FAQItem


class FAQItemSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = FAQItem
        fields = ('id', 'question', 'answer', 'category', 'category_display', 'order')
