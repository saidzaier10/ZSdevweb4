import uuid
from django.db import models
from django.utils import timezone
from services_catalog.models import ProjectType, DesignOption, ComplexityLevel, SupplementaryOption


def generate_quote_number():
    from django.utils import timezone
    year = timezone.now().year
    count = Quote.objects.filter(created_at__year=year).count() + 1
    return f'QT-{year}-{count:04d}'


class Quote(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SENT = 'sent'
    STATUS_VIEWED = 'viewed'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_EXPIRED = 'expired'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Brouillon'),
        (STATUS_SENT, 'Envoyé'),
        (STATUS_VIEWED, 'Consulté'),
        (STATUS_ACCEPTED, 'Accepté'),
        (STATUS_REJECTED, 'Refusé'),
        (STATUS_EXPIRED, 'Expiré'),
    ]

    # Identification
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    quote_number = models.CharField(max_length=20, unique=True, blank=True)

    # Catalogue
    project_type = models.ForeignKey(
        ProjectType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='quotes'
    )
    design_option = models.ForeignKey(
        DesignOption, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='quotes'
    )
    complexity = models.ForeignKey(
        ComplexityLevel, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='quotes'
    )
    options = models.ManyToManyField(SupplementaryOption, blank=True)

    # Informations client
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField(db_index=True)
    client_phone = models.CharField(max_length=20, blank=True)
    client_company = models.CharField(max_length=200, blank=True)
    project_description = models.TextField(blank=True)
    desired_deadline = models.DateField(null=True, blank=True)

    # Prix (dénormalisés pour audit — immuables après création)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    design_supplement = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    complexity_factor = models.DecimalField(max_digits=4, decimal_places=2, default=1)
    options_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_ttc = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Plan de paiement 30/40/30
    installment_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    installment_2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    installment_3 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Statut et cycle de vie
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT, db_index=True)
    valid_until = models.DateField(null=True, blank=True)
    signature_token = models.CharField(max_length=64, blank=True, db_index=True)
    signed_at = models.DateTimeField(null=True, blank=True)

    # PDF
    pdf_file = models.FileField(upload_to='quotes/%Y/%m/', blank=True)

    # Relations
    lead = models.ForeignKey(
        'leads.Lead', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='quotes'
    )

    # Métadonnées
    notes_internal = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    viewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Devis'
        verbose_name_plural = 'Devis'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['client_email']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.quote_number} — {self.client_name} ({self.get_status_display()})'

    def save(self, *args, **kwargs):
        if not self.quote_number:
            self.quote_number = generate_quote_number()
        if not self.valid_until:
            from datetime import timedelta
            self.valid_until = (timezone.now() + timedelta(days=30)).date()
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        from datetime import date
        return self.valid_until and self.valid_until < date.today()


class QuoteEmailLog(models.Model):
    STATUS_SENT = 'sent'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_SENT, 'Envoyé'),
        (STATUS_FAILED, 'Échec'),
    ]

    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='email_logs')
    sent_to = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True)
    message_id = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Log email devis'
        verbose_name_plural = 'Logs emails devis'

    def __str__(self):
        return f'{self.quote.quote_number} → {self.sent_to} ({self.status})'
