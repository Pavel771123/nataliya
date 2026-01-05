"""
Core services module.
Contains base service classes for business logic.
"""

from typing import Any, Optional
from django.db import models, transaction
from django.core.exceptions import ValidationError


class BaseService:
    """
    Base service class for encapsulating business logic.
    Follows the service layer pattern to keep views thin.
    """
    
    model: Optional[models.Model] = None
    
    def __init__(self, model: Optional[models.Model] = None):
        """Initialize service with optional model."""
        if model:
            self.model = model
    
    def get_queryset(self):
        """Get base queryset for the model."""
        if not self.model:
            raise NotImplementedError("Model not specified")
        return self.model.objects.all()
    
    def get_by_id(self, obj_id: Any):
        """Get object by ID."""
        try:
            return self.get_queryset().get(id=obj_id)
        except self.model.DoesNotExist:
            return None
    
    def get_all(self):
        """Get all objects."""
        return self.get_queryset()
    
    def filter(self, **kwargs):
        """Filter objects by kwargs."""
        return self.get_queryset().filter(**kwargs)
    
    @transaction.atomic
    def create(self, **kwargs):
        """Create new object."""
        obj = self.model(**kwargs)
        obj.full_clean()
        obj.save()
        return obj
    
    @transaction.atomic
    def update(self, obj, **kwargs):
        """Update existing object."""
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.full_clean()
        obj.save()
        return obj
    
    @transaction.atomic
    def delete(self, obj):
        """Delete object (hard delete)."""
        obj.delete()
    
    @transaction.atomic
    def soft_delete(self, obj):
        """Soft delete object if supported."""
        if hasattr(obj, 'soft_delete'):
            obj.soft_delete()
        else:
            raise NotImplementedError("Model does not support soft delete")


class CRUDService(BaseService):
    """
    CRUD service with common operations.
    Extends BaseService with additional utility methods.
    """
    
    def exists(self, **kwargs) -> bool:
        """Check if object exists."""
        return self.get_queryset().filter(**kwargs).exists()
    
    def count(self, **kwargs) -> int:
        """Count objects."""
        if kwargs:
            return self.get_queryset().filter(**kwargs).count()
        return self.get_queryset().count()
    
    def get_or_create(self, defaults=None, **kwargs):
        """Get or create object."""
        return self.model.objects.get_or_create(defaults=defaults, **kwargs)
    
    def bulk_create(self, objects_list):
        """Bulk create objects."""
        return self.model.objects.bulk_create(objects_list)
    
    def bulk_update(self, objects_list, fields):
        """Bulk update objects."""
        return self.model.objects.bulk_update(objects_list, fields)
