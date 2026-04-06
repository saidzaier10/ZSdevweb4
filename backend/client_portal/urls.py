from django.urls import path
from .views import ClientProjectListView, ClientProjectDetailView

urlpatterns = [
    path('projects/', ClientProjectListView.as_view(), name='client-projects'),
    path('projects/<uuid:uuid>/', ClientProjectDetailView.as_view(), name='client-project-detail'),
]
