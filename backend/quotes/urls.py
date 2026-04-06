from django.urls import path
from .views import (
    QuoteCreateView, QuoteDetailView, QuoteSendView,
    QuotePdfView, QuoteSignView, PricePreviewView,
)

urlpatterns = [
    path('', QuoteCreateView.as_view(), name='quote-create'),
    path('price-preview/', PricePreviewView.as_view(), name='quote-price-preview'),
    path('<uuid:uuid>/', QuoteDetailView.as_view(), name='quote-detail'),
    path('<uuid:uuid>/send/', QuoteSendView.as_view(), name='quote-send'),
    path('<uuid:uuid>/pdf/', QuotePdfView.as_view(), name='quote-pdf'),
    path('<uuid:uuid>/sign/', QuoteSignView.as_view(), name='quote-sign'),
]
