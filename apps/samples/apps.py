from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class SamplesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.samples'
    verbose_name = _('Образцы проектов')
