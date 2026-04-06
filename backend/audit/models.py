from django.db import models


class AuditRequest(models.Model):
    OBJECTIVE_CHOICES = [
        ('more_traffic', 'Augmenter le trafic'),
        ('more_leads', 'Générer plus de leads'),
        ('better_ux', 'Améliorer l\'expérience utilisateur'),
        ('faster_site', 'Accélérer le site'),
        ('seo', 'Améliorer le référencement'),
        ('mobile', 'Optimiser pour mobile'),
        ('other', 'Autre'),
    ]

    # Contact
    name = models.CharField(max_length=200)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)

    # Site à auditer
    site_url = models.URLField()
    current_issues = models.TextField(blank=True, help_text="Problèmes actuels identifiés")
    objectives = models.JSONField(
        default=list,
        help_text="Liste d'objectifs sélectionnés"
    )
    budget_range = models.CharField(max_length=50, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    additional_info = models.TextField(blank=True)

    # Traitement
    is_processed = models.BooleanField(default=False, db_index=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    internal_notes = models.TextField(blank=True)

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Demande d\'audit'
        verbose_name_plural = 'Demandes d\'audit'

    def __str__(self):
        return f'Audit {self.site_url} — {self.name}'
