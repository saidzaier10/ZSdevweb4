from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from services_catalog.models import ProjectType


class Lead(models.Model):
    SOURCE_QUOTE_WIZARD = 'quote_wizard'
    SOURCE_QUICK_ESTIMATE = 'quick_estimate'
    SOURCE_ROI_CALCULATOR = 'roi_calculator'
    SOURCE_AUDIT_FORM = 'audit_form'
    SOURCE_CONTACT_FORM = 'contact_form'
    SOURCE_SIMULATOR = 'simulator'

    SOURCE_CHOICES = [
        (SOURCE_QUOTE_WIZARD, 'Wizard de devis'),
        (SOURCE_QUICK_ESTIMATE, 'Estimation rapide'),
        (SOURCE_ROI_CALCULATOR, 'Calculateur ROI'),
        (SOURCE_AUDIT_FORM, "Audit gratuit"),
        (SOURCE_CONTACT_FORM, 'Formulaire contact'),
        (SOURCE_SIMULATOR, 'Simulateur de projet'),
    ]

    BUDGET_CHOICES = [
        ('< 1000', 'Moins de 1 000€'),
        ('1000-3000', '1 000€ — 3 000€'),
        ('3000-6000', '3 000€ — 6 000€'),
        ('6000-15000', '6 000€ — 15 000€'),
        ('> 15000', 'Plus de 15 000€'),
    ]

    # Contact
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)

    # Qualification
    source = models.CharField(max_length=30, choices=SOURCE_CHOICES, db_index=True)
    score = models.PositiveSmallIntegerField(
        default=0,
        help_text="Score de qualification 0-100",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, blank=True)
    project_type = models.ForeignKey(
        ProjectType, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='leads'
    )
    notes = models.TextField(blank=True)

    # Conversion
    is_converted = models.BooleanField(default=False, db_index=True)
    converted_at = models.DateTimeField(null=True, blank=True)

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        indexes = [
            models.Index(fields=['is_converted']),
            models.Index(fields=['score']),
        ]

    def __str__(self):
        return f'{self.email} (score: {self.score}, source: {self.source})'
