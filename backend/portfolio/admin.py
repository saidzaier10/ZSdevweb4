from django.contrib import admin
from .models import PortfolioProject, Testimonial


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client_name', 'is_featured', 'is_published', 'order')
    list_filter = ('is_featured', 'is_published')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_company', 'rating', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'rating')
