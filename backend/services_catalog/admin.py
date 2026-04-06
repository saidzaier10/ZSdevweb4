from django.contrib import admin
from .models import ProjectCategory, ProjectType, DesignOption, ComplexityLevel, SupplementaryOption


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'min_days', 'max_days', 'is_active')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DesignOption)
class DesignOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_supplement', 'is_active', 'order')


@admin.register(ComplexityLevel)
class ComplexityLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'multiplier', 'order')


@admin.register(SupplementaryOption)
class SupplementaryOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_recurring', 'is_active', 'order')
    filter_horizontal = ('recommended_for',)
