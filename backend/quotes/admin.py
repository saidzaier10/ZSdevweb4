import csv
from django.contrib import admin, messages
from django.http import HttpResponse
from django.urls import path
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Sum, Count, Avg, Q
from django.shortcuts import render
from .models import Quote, QuoteEmailLog
from services.email_service import EmailService
from services.pdf_service import PdfService
from utils.admin_badges import render_status_badge, QUOTE_STATUS_COLORS, EMAIL_STATUS_COLORS


class QuoteEmailLogInline(admin.TabularInline):
    model = QuoteEmailLog
    extra = 0
    readonly_fields = ('sent_to', 'sent_at', 'subject', 'status', 'error_message')
    can_delete = False
    show_change_link = False


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        'quote_number', 'client_name', 'client_email',
        'project_type_name', 'total_ttc_display',
        'status_badge', 'created_at', 'actions_buttons',
    )
    list_filter = ('status', 'project_type__category', 'created_at', 'valid_until')
    search_fields = ('quote_number', 'client_name', 'client_email', 'client_company')
    readonly_fields = ('uuid', 'quote_number', 'created_at', 'updated_at', 'viewed_at', 'signed_at')
    inlines = [QuoteEmailLogInline]
    date_hierarchy = 'created_at'
    list_per_page = 25
    actions = ['action_send_email', 'action_generate_pdf', 'action_mark_accepted',
               'action_mark_expired', 'action_export_csv']

    fieldsets = (
        ('Identification', {
            'fields': ('uuid', 'quote_number', 'status', 'valid_until', 'signed_at', 'viewed_at')
        }),
        ('Projet', {
            'fields': ('project_type', 'design_option', 'complexity', 'options',
                       'project_description', 'desired_deadline')
        }),
        ('Client', {
            'fields': ('client_name', 'client_email', 'client_phone', 'client_company')
        }),
        ('Tarification', {
            'fields': (
                'base_price', 'design_supplement', 'complexity_factor', 'options_total',
                'subtotal_ht', 'discount_percent', 'discount_amount',
                'vat_rate', 'vat_amount', 'total_ttc',
            ),
            'classes': ('collapse',),
        }),
        ('Plan de paiement 30/40/30', {
            'fields': ('installment_1', 'installment_2', 'installment_3'),
            'classes': ('collapse',),
        }),
        ('Interne', {
            'fields': ('lead', 'notes_internal', 'pdf_file', 'signature_token',
                       'created_at', 'updated_at'),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view),
                 name='quotes_dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        """Vue tableau de bord avec statistiques clés."""
        from django.db.models.functions import TruncMonth
        from leads.models import Lead

        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0)

        # Stats devis
        all_quotes = Quote.objects.all()
        quotes_stats = {
            'total': all_quotes.count(),
            'this_month': all_quotes.filter(created_at__gte=month_start).count(),
            'accepted': all_quotes.filter(status='accepted').count(),
            'pending': all_quotes.filter(status__in=['draft', 'sent', 'viewed']).count(),
            'conversion_rate': 0,
            'total_revenue': all_quotes.filter(status='accepted').aggregate(
                s=Sum('total_ttc'))['s'] or 0,
            'avg_value': all_quotes.filter(status='accepted').aggregate(
                a=Avg('total_ttc'))['a'] or 0,
            'monthly_revenue': all_quotes.filter(
                status='accepted', created_at__gte=month_start
            ).aggregate(s=Sum('total_ttc'))['s'] or 0,
        }
        total = quotes_stats['total']
        if total > 0:
            quotes_stats['conversion_rate'] = round(
                quotes_stats['accepted'] / total * 100, 1)

        # Stats leads
        leads_stats = {
            'total': Lead.objects.count(),
            'this_month': Lead.objects.filter(created_at__gte=month_start).count(),
            'converted': Lead.objects.filter(is_converted=True).count(),
            'hot': Lead.objects.filter(score__gte=60).count(),
            'avg_score': Lead.objects.aggregate(a=Avg('score'))['a'] or 0,
        }

        # Évolution mensuelle (6 derniers mois)
        monthly = (
            all_quotes
            .filter(created_at__gte=now - timezone.timedelta(days=180))
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'), revenue=Sum('total_ttc'))
            .order_by('month')
        )

        # Top types de projets
        top_types = (
            all_quotes
            .filter(project_type__isnull=False)
            .values('project_type__name')
            .annotate(count=Count('id'), revenue=Sum('total_ttc'))
            .order_by('-revenue')[:5]
        )

        # Derniers leads chauds
        hot_leads = Lead.objects.filter(score__gte=50).order_by('-score', '-created_at')[:10]

        context = {
            **self.admin_site.each_context(request),
            'title': 'Dashboard — Zsdevweb',
            'quotes_stats': quotes_stats,
            'leads_stats': leads_stats,
            'monthly_data': list(monthly),
            'top_types': list(top_types),
            'hot_leads': hot_leads,
            'recent_quotes': all_quotes.select_related('project_type').order_by('-created_at')[:10],
        }
        return render(request, 'admin/quotes/dashboard.html', context)

    # ---- Display helpers ----

    def project_type_name(self, obj):
        return obj.project_type.name if obj.project_type else '—'
    project_type_name.short_description = 'Type'

    def total_ttc_display(self, obj):
        return format_html('<strong>{} €</strong>', f'{obj.total_ttc:,.0f}')
    total_ttc_display.short_description = 'Total TTC'
    total_ttc_display.admin_order_field = 'total_ttc'

    def status_badge(self, obj):
        return render_status_badge(obj.status, QUOTE_STATUS_COLORS)
    status_badge.short_description = 'Statut'

    def actions_buttons(self, obj):
        buttons = []
        if obj.status in ('draft', 'viewed'):
            buttons.append(
                f'<a href="/api/v1/quotes/{obj.uuid}/send/" '
                f'style="margin-right:4px;padding:2px 8px;background:#3b82f6;'
                f'color:white;border-radius:4px;font-size:11px;text-decoration:none">'
                f'📧 Email</a>'
            )
        if obj.pdf_file:
            buttons.append(
                f'<a href="/api/v1/quotes/{obj.uuid}/pdf/" target="_blank" '
                f'style="padding:2px 8px;background:#6b7280;'
                f'color:white;border-radius:4px;font-size:11px;text-decoration:none">'
                f'📄 PDF</a>'
            )
        return format_html(''.join(buttons)) if buttons else '—'
    actions_buttons.short_description = 'Actions'

    # ---- Bulk actions ----

    @admin.action(description='📧 Envoyer par email')
    def action_send_email(self, request, queryset):
        sent, failed = 0, 0
        for quote in queryset.exclude(status='accepted'):
            if EmailService.send_quote_to_client(quote):
                sent += 1
            else:
                failed += 1
        if sent:
            self.message_user(request, f'{sent} devis envoyé(s) avec succès.', messages.SUCCESS)
        if failed:
            self.message_user(request, f'{failed} envoi(s) échoué(s).', messages.WARNING)

    @admin.action(description='📄 Générer PDF')
    def action_generate_pdf(self, request, queryset):
        generated = 0
        for quote in queryset:
            if PdfService.generate_quote_pdf(quote):
                generated += 1
        self.message_user(request, f'{generated} PDF généré(s).', messages.SUCCESS)

    @admin.action(description='✅ Marquer comme accepté')
    def action_mark_accepted(self, request, queryset):
        count = queryset.update(status='accepted')
        self.message_user(request, f'{count} devis marqué(s) comme accepté(s).', messages.SUCCESS)

    @admin.action(description='⏰ Marquer comme expiré')
    def action_mark_expired(self, request, queryset):
        count = queryset.filter(status__in=['draft', 'sent', 'viewed']).update(status='expired')
        self.message_user(request, f'{count} devis marqué(s) comme expiré(s).', messages.SUCCESS)

    @admin.action(description='📊 Exporter en CSV')
    def action_export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="devis_export.csv"'
        response.write('\ufeff')  # BOM pour Excel

        writer = csv.writer(response, delimiter=';')
        writer.writerow([
            'Numéro', 'Client', 'Email', 'Société',
            'Type de projet', 'Complexité', 'Statut',
            'HT (€)', 'TVA (€)', 'TTC (€)',
            'Acompte 30%', 'Mi-projet 40%', 'Solde 30%',
            'Date création', 'Valable jusqu\'au',
        ])
        for q in queryset.select_related('project_type', 'complexity'):
            writer.writerow([
                q.quote_number, q.client_name, q.client_email, q.client_company,
                q.project_type.name if q.project_type else '',
                q.complexity.name if q.complexity else '',
                q.get_status_display(),
                str(q.subtotal_ht), str(q.vat_amount), str(q.total_ttc),
                str(q.installment_1), str(q.installment_2), str(q.installment_3),
                q.created_at.strftime('%d/%m/%Y'),
                q.valid_until.strftime('%d/%m/%Y') if q.valid_until else '',
            ])
        return response


@admin.register(QuoteEmailLog)
class QuoteEmailLogAdmin(admin.ModelAdmin):
    list_display = ('quote', 'sent_to', 'sent_at', 'status_badge', 'subject')
    list_filter = ('status', 'sent_at')
    search_fields = ('sent_to', 'quote__quote_number')
    readonly_fields = ('quote', 'sent_to', 'sent_at', 'subject', 'status', 'error_message', 'message_id')

    def status_badge(self, obj):
        return render_status_badge(obj.status, EMAIL_STATUS_COLORS)
    status_badge.short_description = 'Statut'
