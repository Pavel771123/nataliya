"""
Portfolio URL configuration.
"""

from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('category/<slug:category_slug>/', views.ProjectListView.as_view(), name='project_list_by_category'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
]
