import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.db.models import Avg
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'name', 'company',
        'source_badge', 'score_bar',
        'budget_range', 'converted_badge', 'created_at',
    )
    list_filter = ('source', 'is_converted', 'budget_range', 'created_at')
    search_fields = ('email', 'name', 'company')
    readonly_fields = ('created_at', 'updated_at', 'converted_at')
    ordering = ('-score', '-created_at')
    list_per_page = 30
    actions = ['action_mark_converted', 'action_export_csv']

    fieldsets = (
        ('Contact', {
            'fields': ('name', 'email', 'phone', 'company'),
        }),
        ('Qualification', {
            'fields': ('source', 'score', 'budget_range', 'project_type'),
        }),
        ('Conversion', {
            'fields': ('is_converted', 'converted_at', 'quote'),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    # ---- Display helpers ----

    def source_badge(self, obj):
        colors = {
            'quote_wizard':   '#6366f1',
            'estimate':       '#3b82f6',
            'audit_form':     '#8b5cf6',
            'contact_form':   '#06b6d4',
            'portfolio':      '#10b981',
            'direct':         '#6b7280',
        }
        color = colors.get(obj.source, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;'
            'border-radius:10px;font-size:11px">{}</span>',
            color, obj.get_source_display(),
        )
    source_badge.short_description = 'Source'

    def score_bar(self, obj):
        score = int(obj.score)
        if score >= 70:
            color = '#10b981'
        elif score >= 40:
            color = '#f59e0b'
        else:
            color = '#ef4444'
        return format_html(
            '<div style="display:flex;align-items:center;gap:6px">'
            '<div style="width:80px;background:#e5e7eb;border-radius:4px;height:8px">'
            '<div style="width:{}%;background:{};border-radius:4px;height:8px"></div>'
            '</div>'
            '<span style="font-size:11px;font-weight:600;color:{}">{}</span>'
            '</div>',
            min(score, 100), color, color, score,
        )
    score_bar.short_description = 'Score'
    score_bar.admin_order_field = 'score'

    def converted_badge(self, obj):
        if obj.is_converted:
            return format_html(
                '<span style="background:#10b981;color:white;padding:2px 8px;'
                'border-radius:10px;font-size:11px">✓ Converti</span>'
            )
        return format_html(
            '<span style="background:#e5e7eb;color:#6b7280;padding:2px 8px;'
            'border-radius:10px;font-size:11px">En attente</span>'
        )
    converted_badge.short_description = 'Conversion'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project_type', 'quote')

    # ---- Bulk actions ----

    @admin.action(description='✅ Marquer comme converti')
    def action_mark_converted(self, request, queryset):
        from django.utils import timezone
        count = queryset.filter(is_converted=False).update(
            is_converted=True, converted_at=timezone.now()
        )
        self.message_user(request, f'{count} lead(s) marqué(s) comme converti(s).')

    @admin.action(description='📊 Exporter en CSV')
    def action_export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="leads_export.csv"'
        response.write('\ufeff')  # BOM pour Excel

        writer = csv.writer(response, delimiter=';')
        writer.writerow([
            'Nom', 'Email', 'Téléphone', 'Société',
            'Source', 'Score', 'Budget', 'Type de projet',
            'Converti', 'Date création',
        ])
        for lead in queryset.select_related('project_type'):
            writer.writerow([
                lead.name, lead.email, lead.phone or '', lead.company or '',
                lead.get_source_display(), lead.score,
                lead.budget_range or '', lead.project_type.name if lead.project_type else '',
                'Oui' if lead.is_converted else 'Non',
                lead.created_at.strftime('%d/%m/%Y'),
            ])
        return response
