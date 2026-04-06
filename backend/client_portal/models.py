import uuid
from django.db import models
from django.conf import settings


class ClientProject(models.Model):
    """
    Projet client visible dans l'espace client.
    Lié à un devis accepté et à un utilisateur.
    """
    STATUS_CHOICES = [
        ('briefing',     'Briefing'),
        ('design',       'Design'),
        ('development',  'Développement'),
        ('review',       'Révision'),
        ('delivered',    'Livré'),
        ('maintenance',  'Maintenance'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
    )
    quote = models.OneToOneField(
        'quotes.Quote',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='project',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='briefing')
    progress_percent = models.PositiveSmallIntegerField(default=0)  # 0-100

    # Dates clés
    started_at = models.DateField(null=True, blank=True)
    estimated_delivery = models.DateField(null=True, blank=True)
    delivered_at = models.DateField(null=True, blank=True)

    # URL du site livré
    site_url = models.URLField(blank=True)

    # Accès repo (optionnel)
    repo_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Projet client'
        verbose_name_plural = 'Projets clients'

    def __str__(self):
        return f'{self.title} — {self.client.email}'


class ProjectUpdate(models.Model):
    """
    Mise à jour de progression visible par le client.
    """
    TYPE_CHOICES = [
        ('progress', 'Avancement'),
        ('milestone', 'Jalon'),
        ('delivery', 'Livraison'),
        ('feedback', 'Demande de retour'),
        ('info', 'Information'),
    ]

    project = models.ForeignKey(
        ClientProject, on_delete=models.CASCADE, related_name='updates'
    )
    update_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='progress')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_visible_to_client = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mise à jour projet'

    def __str__(self):
        return f'{self.project.title} — {self.title}'


class ProjectDocument(models.Model):
    """
    Documents partagés avec le client (maquettes, contrats, livrables…).
    """
    TYPE_CHOICES = [
        ('contract',  'Contrat'),
        ('mockup',    'Maquette'),
        ('deliverable', 'Livrable'),
        ('invoice',   'Facture'),
        ('other',     'Autre'),
    ]

    project = models.ForeignKey(
        ClientProject, on_delete=models.CASCADE, related_name='documents'
    )
    doc_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='client_docs/%Y/%m/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Document projet'

    def __str__(self):
        return f'{self.project.title} — {self.name}'
