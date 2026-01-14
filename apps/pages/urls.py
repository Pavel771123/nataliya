"""
Pages URL configuration.
"""

from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('sketch/', views.SketchView.as_view(), name='sketch'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
]
