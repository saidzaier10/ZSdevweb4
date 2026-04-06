from django.db import models
from django.utils.text import slugify


class PortfolioProject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    tech_stack = models.JSONField(
        default=list,
        help_text="Liste de technologies (ex: ['Vue.js', 'Django', 'PostgreSQL'])"
    )
    image = models.ImageField(upload_to='portfolio/', blank=True)
    image_secondary = models.ImageField(upload_to='portfolio/', blank=True)
    url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    client_name = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_published = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Projet portfolio'
        verbose_name_plural = 'Projets portfolio'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)
    client_company = models.CharField(max_length=200, blank=True)
    client_role = models.CharField(max_length=200, blank=True)
    client_avatar = models.ImageField(upload_to='testimonials/', blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    project = models.ForeignKey(
        PortfolioProject, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='testimonials'
    )
    is_active = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Témoignage'
        verbose_name_plural = 'Témoignages'

    def __str__(self):
        return f'{self.client_name} ({self.client_company})'
