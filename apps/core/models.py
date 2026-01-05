"""
Core models module.
Contains base abstract models for use across the project.
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Abstract base model with timestamp fields.
    Provides created_at and updated_at fields.
    """
    
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True,
        help_text=_('Дата и время создания записи')
    )
    updated_at = models.DateTimeField(
        _('Дата обновления'),
        auto_now=True,
        help_text=_('Дата и время последнего обновления записи')
    )
    
    class Meta:
        abstract = True
        ordering = ['-created_at']


class UUIDModel(models.Model):
    """
    Abstract base model with UUID primary key.
    Uses UUID4 for unique identification.
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID')
    )
    
    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base model with soft delete functionality.
    Provides is_deleted field and custom manager.
    """
    
    is_deleted = models.BooleanField(
        _('Удалено'),
        default=False,
        help_text=_('Отметка об удалении записи')
    )
    deleted_at = models.DateTimeField(
        _('Дата удаления'),
        null=True,
        blank=True,
        help_text=_('Дата и время удаления записи')
    )
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        """Soft delete the object."""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        """Restore soft deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class BaseModel(TimeStampedModel, UUIDModel, SoftDeleteModel):
    """
    Base abstract model combining all common functionality.
    Includes timestamps, UUID primary key, and soft delete.
    """
    
    class Meta:
        abstract = True
