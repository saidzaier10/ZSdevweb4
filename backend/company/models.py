from django.db import models


class CompanySettings(models.Model):
    """
    Modèle singleton — une seule ligne en base.
    Le pk=1 est forcé dans save() pour garantir l'unicité.
    """
    company_name = models.CharField(max_length=200, default='Zsdevweb')
    tagline = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    # Contact
    email = models.EmailField(default='contact@zsdevweb.fr')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='France')

    # Légal
    siret = models.CharField(max_length=20, blank=True)
    vat_number = models.CharField(max_length=30, blank=True)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=20.00)
    legal_form = models.CharField(max_length=100, blank=True, default='Auto-entrepreneur')

    # Branding
    logo = models.ImageField(upload_to='company/', blank=True)
    favicon = models.ImageField(upload_to='company/', blank=True)

    # Réseaux sociaux
    social_linkedin = models.URLField(blank=True)
    social_github = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)

    # Config quote
    quote_validity_days = models.PositiveIntegerField(default=30)
    quote_footer_text = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Paramètres société'
        verbose_name_plural = 'Paramètres société'

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        """Récupère (ou crée) le singleton avec mise en cache Redis."""
        from django.core.cache import cache
        cached = cache.get('company_settings')
        if cached is None:
            obj, _ = cls.objects.get_or_create(pk=1)
            cache.set('company_settings', obj, timeout=3600)
            return obj
        return cached
