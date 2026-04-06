from django.db import models


class ContactRequest(models.Model):
    SUBJECT_CHOICES = [
        ('project', 'Nouveau projet'),
        ('quote', 'Demande de devis'),
        ('partnership', 'Partenariat'),
        ('support', 'Support'),
        ('other', 'Autre'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='project')
    message = models.TextField()
    is_processed = models.BooleanField(default=False, db_index=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Demande de contact'
        verbose_name_plural = 'Demandes de contact'

    def __str__(self):
        return f'{self.name} — {self.get_subject_display()} ({self.email})'
