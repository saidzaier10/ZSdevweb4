from django.urls import path
from .views import (
    ProjectCategoryListView,
    ProjectTypeListView,
    DesignOptionListView,
    ComplexityLevelListView,
    SupplementaryOptionListView,
)

urlpatterns = [
    path('categories/', ProjectCategoryListView.as_view(), name='catalog-categories'),
    path('project-types/', ProjectTypeListView.as_view(), name='catalog-project-types'),
    path('design-options/', DesignOptionListView.as_view(), name='catalog-design-options'),
    path('complexity/', ComplexityLevelListView.as_view(), name='catalog-complexity'),
    path('options/', SupplementaryOptionListView.as_view(), name='catalog-options'),
]
