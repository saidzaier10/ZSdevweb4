from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.core.cache import cache
from django.db import connection
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


def _run_readiness_checks():
    checks = {
        'database': {'ok': True},
        'cache': {'ok': True},
    }

    status_code = 200

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except Exception as exc:
        checks['database'] = {'ok': False, 'detail': str(exc)}
        status_code = 503

    try:
        cache_key = 'healthcheck:ping'
        cache.set(cache_key, 'pong', timeout=5)
        if cache.get(cache_key) != 'pong':
            raise RuntimeError('Cache read/write mismatch')
    except Exception as exc:
        checks['cache'] = {'ok': False, 'detail': str(exc)}
        status_code = 503

    return status_code, checks


def health_check(request):
    status_code, checks = _run_readiness_checks()
    return JsonResponse(
        {
            'status': 'ok' if status_code == 200 else 'degraded',
            'checks': checks,
            'mode': 'readiness',
        },
        status=status_code,
    )


def liveness_check(request):
    return JsonResponse({'status': 'ok', 'mode': 'liveness'}, status=200)


def readiness_check(request):
    status_code, checks = _run_readiness_checks()
    return JsonResponse(
        {
            'status': 'ok' if status_code == 200 else 'degraded',
            'checks': checks,
            'mode': 'readiness',
        },
        status=status_code,
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/health/', health_check, name='health'),
    path('api/v1/health/liveness/', liveness_check, name='health-liveness'),
    path('api/v1/health/readiness/', readiness_check, name='health-readiness'),
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
    urlpatterns += [
        path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
else:
    urlpatterns += [
        path('api/v1/schema/', staff_member_required(SpectacularAPIView.as_view()), name='schema'),
        path('api/v1/docs/', staff_member_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
        path('api/v1/redoc/', staff_member_required(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
