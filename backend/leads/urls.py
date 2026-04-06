from django.urls import path
from .views import LeadCaptureView

urlpatterns = [
    path('', LeadCaptureView.as_view(), name='lead-capture'),
]
