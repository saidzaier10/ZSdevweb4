from django.db import models


class FAQItem(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'Général'),
        ('pricing', 'Tarifs'),
        ('process', 'Processus'),
        ('technical', 'Technique'),
        ('support', 'Support'),
    ]

    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.question[:80]
