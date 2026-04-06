from django.contrib import admin
from .models import AuditRequest


@admin.register(AuditRequest)
class AuditRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'site_url', 'is_processed', 'created_at')
    list_filter = ('is_processed',)
    search_fields = ('name', 'email', 'site_url')
