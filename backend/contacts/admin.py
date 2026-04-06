from django.contrib import admin
from .models import ContactRequest


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_processed', 'created_at')
    list_filter = ('subject', 'is_processed')
    search_fields = ('name', 'email')
