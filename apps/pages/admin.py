"""
Pages admin configuration.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)
# from .models import Page, Testimonial
from .models import Testimonial, PriceService

@admin.register(PriceService)
class PriceServiceAdmin(admin.ModelAdmin):
    """
    Admin interface for PriceService model.
    """
    list_display = ['title', 'price', 'is_active', 'order']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'price']
    list_filter = ['is_active']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Admin interface for Testimonial model.
    """
    
    list_display = [
        'client_name',
        'rating',
        'is_published',
        'order',
        'created_at'
    ]
    list_filter = [
        'is_published',
        'rating',
        'created_at'
    ]
    search_fields = [
        'client_name',
        'text',
        'client_info'
    ]
    list_editable = [
        'is_published',
        'order',
        'rating'
    ]
    
    def get_queryset(self, request):
        """Override queryset to exclude soft-deleted items by default."""
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)



# @admin.register(Page)
# class PageAdmin(admin.ModelAdmin):
#     """
#     Admin interface for Page model.
#     """
#     
#     list_display = [
#         'title',
#         'slug',
#         'is_published',
#         'order',
#         'created_at',
#         'updated_at'
#     ]
#     list_filter = [
#         'is_published',
#         'created_at',
#         'updated_at'
#     ]
#     search_fields = [
#         'title',
#         'slug',
#         'content',
#         'meta_description'
#     ]
#     prepopulated_fields = {
#         'slug': ('title',)
#     }
#     list_editable = [
#         'is_published',
#         'order'
#     ]
#     readonly_fields = [
#         'id',
#         'created_at',
#         'updated_at'
#     ]
#     
#     fieldsets = (
#         (_('Основная информация'), {
#             'fields': (
#                 'title',
#                 'slug',
#                 'content',
#                 'is_published',
#                 'order'
#             )
#         }),
#         (_('SEO'), {
#             'fields': (
#                 'meta_description',
#                 'meta_keywords'
#             ),
#             'classes': ('collapse',)
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
#     
#     def get_queryset(self, request):
#         """Override queryset to exclude soft-deleted items by default."""
#         qs = super().get_queryset(request)
#         return qs.filter(is_deleted=False)
