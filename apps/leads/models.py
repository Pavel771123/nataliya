from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

class Lead(models.Model):
    """
    Model for storing contact form leads.
    """
    name = models.CharField(
        _('Имя'),
        max_length=100
    )
    phone = models.CharField(
        _('Телефон'),
        max_length=20
    )
    description = models.TextField(
        _('Описание проекта'),
        blank=True,
        null=True
    )
    file = models.FileField(
        _('Файл (PDF)'),
        upload_to='leads/files/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('Заявка')
        verbose_name_plural = _('Заявки')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.phone}"
