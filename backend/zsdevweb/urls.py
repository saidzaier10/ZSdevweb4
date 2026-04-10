from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.contrib.sitemaps.views import sitemap
from .sitemaps import sitemaps


def health_check(_request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('api/v1/health/', health_check, name='health'),
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/catalog/', include('services_catalog.urls')),
    path('api/v1/quotes/', include('quotes.urls')),
    path('api/v1/leads/', include('leads.urls')),
    path('api/v1/contacts/', include('contacts.urls')),
    path('api/v1/audit/', include('audit.urls')),
    path('api/v1/portfolio/', include('portfolio.urls')),
    path('api/v1/marketing/', include('marketing.urls')),
    path('api/v1/company/', include('company.urls')),
    path('api/v1/client/', include('client_portal.urls')),
]

if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
    urlpatterns += [
        # Schéma OpenAPI brut (JSON/YAML)
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        # Swagger UI interactif
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        # ReDoc (alternative plus lisible)
        path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
