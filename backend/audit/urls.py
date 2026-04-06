from django.urls import path
from .views import AuditRequestCreateView

urlpatterns = [
    path('', AuditRequestCreateView.as_view(), name='audit-create'),
]
