"""
Portfolio admin configuration.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Project, ProjectCategory, ProjectImage, ProjectCharacteristic


class ProjectImageInline(admin.TabularInline):
    """Inline admin for project images."""
    
    model = ProjectImage
    extra = 5
    fields = ['image', 'image_preview', 'title', 'order', 'is_cover']
    readonly_fields = ['image_preview', 'created_at']
    
    def image_preview(self, obj):
        if obj.image:
            from django.utils.html import mark_safe
            return mark_safe(f'<img src="{obj.image.url}" style="height: 50px; border-radius: 4px;" />')
        return ""
    image_preview.short_description = "Превью"


class ProjectCharacteristicInline(admin.TabularInline):
    """Inline admin for project characteristics."""
    
    model = ProjectCharacteristic
    extra = 1
    fields = ['name', 'value', 'order']


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    """Admin interface for ProjectCategory model."""
    
    list_display = ['name', 'slug', 'order', 'created_at']
    list_editable = ['order']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'slug', 'description', 'order')
        }),
        (_('Системная информация'), {
            'fields': ('id', 'created_at', 'updated_at', 'is_deleted'),
            'classes': ('collapse',)
        })
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin interface for Project model."""
    
    list_display = [
        'title',
        'category',
        'year',
        'area',
        'is_published',
        'is_featured',
        'order',
        'created_at'
    ]
    list_filter = [
        'is_published',
        'is_featured',
        'category',
        'year',
        'created_at'
    ]
    search_fields = [
        'title',
        'description',
        'short_description',
        'client_type'
    ]
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'is_featured', 'order']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [ProjectImageInline, ProjectCharacteristicInline]
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': (
                'title',
                'slug',
                'category',
                'year',
                'area',
                'client_type'
            )
        }),
        (_('Описание'), {
            'fields': (
                'short_description',
                'description'
            )
        }),
        (_('Настройки публикации'), {
            'fields': (
                'is_published',
                'is_featured',
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



# class ProjectImageAdmin(admin.ModelAdmin):
#     """Admin interface for ProjectImage model."""
    
#     list_display = [
#         'project',
#         'title',
#         'is_cover',
#         'order',
#         'created_at'
#     ]
#     list_filter = ['is_cover', 'project', 'created_at']
#     search_fields = ['title', 'description', 'project__title']
#     list_editable = ['order', 'is_cover']
#     readonly_fields = ['id', 'created_at', 'updated_at']
    
#     fieldsets = (
#         (_('Основная информация'), {
#             'fields': (
#                 'project',
#                 'image',
#                 'title',
#                 'description',
#                 'order',
#                 'is_cover'
#             )
#         }),
#         (_('Системная информация'), {
#             'fields': (
#                 'id',
#                 'created_at',
#                 'updated_at',
#                 'is_deleted'
#             ),
#             'classes': ('collapse',)
#         })
#     )
