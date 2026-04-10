from django.urls import path
from .views import PortfolioProjectListView, PortfolioProjectDetailView, TestimonialListView

urlpatterns = [
    path('projects/', PortfolioProjectListView.as_view(), name='portfolio-list'),
    path('projects/<slug:slug>/', PortfolioProjectDetailView.as_view(), name='portfolio-detail'),
    path('testimonials/', TestimonialListView.as_view(), name='testimonials-list'),
]
