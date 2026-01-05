"""
Pages admin configuration.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """
    Admin interface for Page model.
    """
    
    list_display = [
        'title',
        'slug',
        'is_published',
        'order',
        'created_at',
        'updated_at'
    ]
    list_filter = [
        'is_published',
        'created_at',
        'updated_at'
    ]
    search_fields = [
        'title',
        'slug',
        'content',
        'meta_description'
    ]
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_editable = [
        'is_published',
        'order'
    ]
    readonly_fields = [
        'id',
        'created_at',
        'updated_at'
    ]
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': (
                'title',
                'slug',
                'content',
                'is_published',
                'order'
            )
        }),
        (_('SEO'), {
            'fields': (
                'meta_description',
                'meta_keywords'
            ),
            'classes': ('collapse',)
        }),
        (_('Системная информация'), {
            'fields': (
                'id',
                'created_at',
                'updated_at',
                'is_deleted'
            ),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """Override queryset to exclude soft-deleted items by default."""
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)
