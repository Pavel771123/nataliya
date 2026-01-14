from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Sample, SampleImage

class SampleImageInline(admin.TabularInline):
    model = SampleImage
    extra = 1

@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'year', 'area', 'is_published', 'order']
    list_editable = ['is_published', 'order']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SampleImageInline]
    search_fields = ['title', 'description']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'is_published', 'order')
        }),
        (_('Характеристики'), {
            'fields': ('year', 'area', 'client_type', 'price_info', 'pdf_file', 'description')
        }),
        (_('SEO'), {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
