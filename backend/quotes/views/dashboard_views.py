from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum
from django.utils import timezone

from quotes.models import Quote
from client_portal.models import ClientProject
from audit.models import AuditRequest

ACTIVE_STATUSES = ['briefing', 'design', 'development', 'review']


class DashboardStatsView(APIView):
    """
    Tableau de bord admin : KPIs, devis récents, projets actifs.
    Accès réservé au staff (is_staff=True).
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        all_quotes     = Quote.objects.all()
        accepted       = all_quotes.filter(status=Quote.STATUS_ACCEPTED)
        pending        = all_quotes.filter(status__in=[Quote.STATUS_DRAFT, Quote.STATUS_SENT, Quote.STATUS_VIEWED])
        total          = all_quotes.count()
        total_accepted = accepted.count()

        recent_quotes   = all_quotes.select_related('project_type').order_by('-created_at')[:10]
        active_projects = (
            ClientProject.objects
            .select_related('client')
            .filter(status__in=ACTIVE_STATUSES)
            .order_by('-updated_at')[:10]
        )
        recent_audits   = AuditRequest.objects.order_by('-created_at')[:10]
        audits_pending  = AuditRequest.objects.filter(is_processed=False).count()

        return Response({
            'kpis': {
                'quotes_total':       total,
                'quotes_this_month':  all_quotes.filter(created_at__gte=month_start).count(),
                'quotes_pending':     pending.count(),
                'quotes_accepted':    total_accepted,
                'conversion_rate':    round(total_accepted / total * 100, 1) if total else 0,
                'revenue_total':      str(accepted.aggregate(s=Sum('total_ttc'))['s'] or 0),
                'revenue_this_month': str(accepted.filter(created_at__gte=month_start).aggregate(s=Sum('total_ttc'))['s'] or 0),
                'projects_active':    ClientProject.objects.filter(status__in=ACTIVE_STATUSES).count(),
                'audits_pending':     audits_pending,
            },
            'recent_quotes': [
                {
                    'uuid':           str(q.uuid),
                    'quote_number':   q.quote_number,
                    'client_name':    q.client_name,
                    'client_company': q.client_company,
                    'total_ttc':      str(q.total_ttc),
                    'status':         q.status,
                    'status_display': q.get_status_display(),
                    'created_at':     q.created_at.isoformat(),
                }
                for q in recent_quotes
            ],
            'active_projects': [
                {
                    'uuid':             str(p.uuid),
                    'title':            p.title,
                    'client_email':     p.client.email,
                    'status':           p.status,
                    'status_display':   p.get_status_display(),
                    'progress_percent': p.progress_percent,
                }
                for p in active_projects
            ],
            'recent_audits': [
                {
                    'id':           a.id,
                    'name':         a.name,
                    'email':        a.email,
                    'company':      a.company,
                    'site_url':     a.site_url,
                    'objectives':   a.objectives,
                    'is_processed': a.is_processed,
                    'created_at':   a.created_at.isoformat(),
                }
                for a in recent_audits
            ],
        })
