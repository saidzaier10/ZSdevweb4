from django.urls import path
from .views import PortfolioProjectListView, TestimonialListView

urlpatterns = [
    path('projects/', PortfolioProjectListView.as_view(), name='portfolio-list'),
    path('testimonials/', TestimonialListView.as_view(), name='testimonials-list'),
]
