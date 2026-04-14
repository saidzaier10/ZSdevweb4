import logging
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

from quotes.models import Quote
from services.pdf_service import PdfService
from ._helpers import is_token_valid

logger = logging.getLogger(__name__)


class QuotePdfView(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(ratelimit(key='ip', rate='20/m', method='GET', block=True))
    def get(self, request, uuid):
        try:
            quote = Quote.objects.get(uuid=uuid)
        except Quote.DoesNotExist:
            return Response({'detail': 'Devis non trouvé.'}, status=404)

        token = request.query_params.get('token', '')
        if not is_token_valid(token, quote.signature_token) and not request.user.is_authenticated:
            logger.warning('quote_pdf_access_denied quote=%s ip=%s', quote.uuid, request.META.get('REMOTE_ADDR'))
            return Response({'detail': 'Accès refusé.'}, status=403)

        if not quote.pdf_file:
            PdfService.generate_quote_pdf(quote)

        if not quote.pdf_file:
            return Response({'detail': 'PDF non disponible.'}, status=503)

        from django.conf import settings as django_settings
        if not django_settings.DEBUG:
            from django.http import HttpResponse
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Devis_{quote.quote_number}.pdf"'
            response['X-Accel-Redirect'] = f'/media/{quote.pdf_file.name}'
            return response

        return FileResponse(
            quote.pdf_file.open('rb'),
            content_type='application/pdf',
            as_attachment=True,
            filename=f'Devis_{quote.quote_number}.pdf',
        )
