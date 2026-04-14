"""
PdfService — Génération de PDF avec WeasyPrint.
"""
import logging
import os
from io import BytesIO
from django.template.loader import render_to_string
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone

logger = logging.getLogger(__name__)


class PdfService:

    @staticmethod
    def generate_quote_pdf(quote) -> bool:
        """
        Génère le PDF du devis et le sauvegarde sur le modèle Quote.
        Retourne True si succès.
        """
        try:
            from weasyprint import HTML, CSS

            context = {
                'quote': quote,
                'options': quote.options.all(),
                'company': settings.COMPANY_NAME if hasattr(settings, 'COMPANY_NAME') else 'Zsdevweb',
            }

            html_string = render_to_string('pdf/quote.html', context)
            html = HTML(string=html_string, base_url=settings.STATIC_ROOT)

            pdf_bytes = html.write_pdf()

            filename = f'Devis_{quote.quote_number}.pdf'
            quote.pdf_file.save(filename, ContentFile(pdf_bytes), save=False)
            quote.pdf_generated_at = timezone.now()
            quote.save(update_fields=['pdf_file', 'pdf_generated_at'])

            return True

        except ImportError:
            logger.warning('WeasyPrint non installé — PDF non généré')
            return False
        except Exception as e:
            logger.error(f'Erreur génération PDF devis {quote.quote_number}: {e}')
            return False
