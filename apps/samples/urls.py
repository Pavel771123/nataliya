from django.urls import path
from . import views

app_name = 'samples'

urlpatterns = [
    path('', views.SampleListView.as_view(), name='sample_list'),
    path('<slug:slug>/', views.SampleDetailView.as_view(), name='sample_detail'),
]
