from django.contrib import admin
from django.utils.html import format_html
from .models import Quote, QuoteEmailLog


class QuoteEmailLogInline(admin.TabularInline):
    model = QuoteEmailLog
    extra = 0
    readonly_fields = ('sent_to', 'sent_at', 'subject', 'status', 'error_message')
    can_delete = False


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('quote_number', 'client_name', 'client_email', 'project_type',
                    'total_ttc_display', 'status_badge', 'created_at')
    list_filter = ('status', 'project_type__category', 'created_at')
    search_fields = ('quote_number', 'client_name', 'client_email', 'client_company')
    readonly_fields = ('uuid', 'quote_number', 'created_at', 'updated_at')
    inlines = [QuoteEmailLogInline]
    fieldsets = (
        ('Identification', {'fields': ('uuid', 'quote_number', 'status', 'valid_until')}),
        ('Projet', {'fields': ('project_type', 'design_option', 'complexity', 'options', 'project_description')}),
        ('Client', {'fields': ('client_name', 'client_email', 'client_phone', 'client_company', 'desired_deadline')}),
        ('Prix', {'fields': ('base_price', 'design_supplement', 'complexity_factor', 'options_total',
                             'subtotal_ht', 'discount_percent', 'discount_amount',
                             'vat_rate', 'vat_amount', 'total_ttc')}),
        ('Paiement 30/40/30', {'fields': ('installment_1', 'installment_2', 'installment_3')}),
        ('Interne', {'fields': ('lead', 'notes_internal', 'created_at', 'updated_at')}),
    )

    def total_ttc_display(self, obj):
        return f'{obj.total_ttc} €'
    total_ttc_display.short_description = 'Total TTC'

    def status_badge(self, obj):
        colors = {
            'draft': '#gray', 'sent': '#3b82f6', 'viewed': '#8b5cf6',
            'accepted': '#10b981', 'rejected': '#ef4444', 'expired': '#f59e0b',
        }
        color = colors.get(obj.status, '#gray')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Statut'
