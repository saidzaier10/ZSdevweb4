from django.contrib import admin
from django.utils.html import format_html
from .models import ClientProject, ProjectUpdate, ProjectDocument


class ProjectUpdateInline(admin.TabularInline):
    model = ProjectUpdate
    extra = 1
    fields = ('update_type', 'title', 'content', 'is_visible_to_client')


class ProjectDocumentInline(admin.TabularInline):
    model = ProjectDocument
    extra = 0
    fields = ('doc_type', 'name', 'file', 'description')
    readonly_fields = ('uploaded_at',)


@admin.register(ClientProject)
class ClientProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'client_email', 'status_badge',
        'progress_bar', 'estimated_delivery', 'updated_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'client__email', 'client__username')
    readonly_fields = ('uuid', 'created_at', 'updated_at')
    inlines = [ProjectUpdateInline, ProjectDocumentInline]

    fieldsets = (
        ('Identification', {'fields': ('uuid', 'title', 'description', 'client', 'quote')}),
        ('Progression', {'fields': ('status', 'progress_percent')}),
        ('Dates', {'fields': ('started_at', 'estimated_delivery', 'delivered_at')}),
        ('Liens', {'fields': ('site_url', 'repo_url')}),
        ('Métadonnées', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def client_email(self, obj):
        return obj.client.email
    client_email.short_description = 'Client'

    def status_badge(self, obj):
        colors = {
            'briefing':    '#6b7280',
            'design':      '#8b5cf6',
            'development': '#3b82f6',
            'review':      '#f59e0b',
            'delivered':   '#10b981',
            'maintenance': '#06b6d4',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;'
            'border-radius:12px;font-size:11px;font-weight:600">{}</span>',
            color, obj.get_status_display(),
        )
    status_badge.short_description = 'Statut'

    def progress_bar(self, obj):
        pct = obj.progress_percent
        color = '#10b981' if pct >= 80 else '#3b82f6' if pct >= 40 else '#f59e0b'
        return format_html(
            '<div style="display:flex;align-items:center;gap:8px">'
            '<div style="width:100px;background:#e5e7eb;border-radius:4px;height:8px">'
            '<div style="width:{}%;background:{};border-radius:4px;height:8px"></div>'
            '</div><span style="font-size:11px;font-weight:600">{}</span></div>',
            pct, color, f'{pct}%',
        )
    progress_bar.short_description = 'Progression'
