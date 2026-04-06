from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'source', 'score', 'budget_range', 'is_converted', 'created_at')
    list_filter = ('source', 'is_converted', 'created_at')
    search_fields = ('email', 'name', 'company')
    readonly_fields = ('created_at', 'updated_at', 'converted_at')
    ordering = ('-score', '-created_at')
