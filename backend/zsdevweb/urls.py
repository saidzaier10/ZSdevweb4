from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('admin/', admin.site.urls),
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
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
