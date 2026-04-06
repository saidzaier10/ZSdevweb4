from django.db import models


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Nom d'icône (ex: heroicons)")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Catégorie de projet'
        verbose_name_plural = 'Catégories de projet'

    def __str__(self):
        return self.name


class ProjectType(models.Model):
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.CASCADE, related_name='project_types'
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_days = models.PositiveIntegerField(default=7)
    max_days = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Type de projet'
        verbose_name_plural = 'Types de projet'

    def __str__(self):
        return f'{self.category.name} — {self.name}'


class DesignOption(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price_supplement = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Montant à ajouter au prix de base (HT)"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Option de design'
        verbose_name_plural = 'Options de design'

    def __str__(self):
        return f'{self.name} (+{self.price_supplement}€)'


class ComplexityLevel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    multiplier = models.DecimalField(
        max_digits=4, decimal_places=2,
        help_text="Multiplicateur appliqué au sous-total (ex: 1.3)"
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Niveau de complexité'
        verbose_name_plural = 'Niveaux de complexité'

    def __str__(self):
        return f'{self.name} (×{self.multiplier})'


class SupplementaryOption(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_recurring = models.BooleanField(
        default=False,
        help_text="Tarif mensuel récurrent (maintenance, etc.)"
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    recommended_for = models.ManyToManyField(
        ProjectType, blank=True, related_name='recommended_options',
        help_text="Types de projets pour lesquels cette option est recommandée"
    )

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Option supplémentaire'
        verbose_name_plural = 'Options supplémentaires'

    def __str__(self):
        suffix = '/mois' if self.is_recurring else ''
        return f'{self.name} ({self.price}€{suffix})'
