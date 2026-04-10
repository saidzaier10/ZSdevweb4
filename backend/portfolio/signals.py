"""
Signaux portfolio — génère des versions WebP des images uploadées via Pillow.
Pas de champ supplémentaire en base, le fichier .webp est créé à côté de l'original.
"""
import logging
import os

from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _generate_webp(image_field):
    """Convertit un ImageField Django en WebP (même dossier, extension .webp)."""
    if not image_field:
        return

    try:
        from PIL import Image

        original_path = image_field.path
        webp_path = os.path.splitext(original_path)[0] + '.webp'

        # Ne regénère pas si le webp est déjà à jour
        if os.path.exists(webp_path):
            orig_mtime = os.path.getmtime(original_path)
            webp_mtime = os.path.getmtime(webp_path)
            if webp_mtime >= orig_mtime:
                return

        with Image.open(original_path) as img:
            # Convertir en RGB si nécessaire (PNG RGBA → WebP sans transparence perd des infos)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGBA')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(webp_path, 'WEBP', quality=85, method=6)
            logger.debug('WebP généré : %s', webp_path)
    except Exception as exc:
        logger.warning('Impossible de générer le WebP pour %s : %s', image_field.name, exc)


@receiver(post_save, sender='portfolio.PortfolioProject')
def generate_portfolio_webp(sender, instance, **kwargs):
    _generate_webp(instance.image)
    _generate_webp(instance.image_secondary)


@receiver(post_save, sender='portfolio.Testimonial')
def generate_testimonial_webp(sender, instance, **kwargs):
    _generate_webp(instance.client_avatar)
