from django.urls import path
from .views import LeadCreateView

app_name = 'leads'

urlpatterns = [
    path('submit/', LeadCreateView.as_view(), name='submit'),
]
