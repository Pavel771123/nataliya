"""
Pages application configuration.
"""

from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Configuration for the pages application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pages'
    verbose_name = 'Страницы'
