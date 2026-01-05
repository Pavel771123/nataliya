"""
Core mixins module.
Contains reusable mixins for models and views.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class TimestampMixin(models.Model):
    """
    Mixin for adding timestamp fields to models.
    """
    
    created_at = models.DateTimeField(
        _('Дата создания'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Дата обновления'),
        auto_now=True
    )
    
    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """
    Mixin for adding soft delete functionality.
    """
    
    is_deleted = models.BooleanField(
        _('Удалено'),
        default=False
    )
    deleted_at = models.DateTimeField(
        _('Дата удаления'),
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        """Mark object as deleted."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        """Restore deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class PublishableMixin(models.Model):
    """
    Mixin for adding publish/draft status to models.
    """
    
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Черновик')),
        (STATUS_PUBLISHED, _('Опубликовано')),
    ]
    
    status = models.CharField(
        _('Статус'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )
    published_at = models.DateTimeField(
        _('Дата публикации'),
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True
    
    def publish(self):
        """Publish the object."""
        self.status = self.STATUS_PUBLISHED
        if not self.published_at:
            self.published_at = timezone.now()
        self.save()
    
    def unpublish(self):
        """Unpublish the object."""
        self.status = self.STATUS_DRAFT
        self.save()
    
    @property
    def is_published(self):
        """Check if object is published."""
        return self.status == self.STATUS_PUBLISHED
