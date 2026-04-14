from .quote_views import QuoteCreateView, QuoteDetailView, QuoteSendView
from .pdf_views import QuotePdfView
from .sign_views import QuoteSignView
from .price_views import PricePreviewView
from .dashboard_views import DashboardStatsView

__all__ = [
    'QuoteCreateView',
    'QuoteDetailView',
    'QuoteSendView',
    'QuotePdfView',
    'QuoteSignView',
    'PricePreviewView',
    'DashboardStatsView',
]
