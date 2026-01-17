"""
Portfolio models module.
Contains models for managing portfolio projects.
"""

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


@receiver([post_save, post_delete], sender='portfolio.Project')
@receiver([post_save, post_delete], sender='portfolio.ProjectCategory')
@receiver([post_save, post_delete], sender='portfolio.ProjectImage')
def clear_portfolio_cache(sender, **kwargs):
    """Clear portfolio cache when any related model changes."""
    cache.clear()


class ProjectCategory(BaseModel):
    """
    Category for portfolio projects.
    """
    
    name = models.CharField(
        _('Название'),
        max_length=100,
        help_text=_('Название категории')
    )
    slug = models.SlugField(
        _('URL-адрес'),
        max_length=100,
        unique=True,
        help_text=_('Уникальный URL-адрес категории')
    )
    description = models.TextField(
        _('Описание'),
        blank=True,
        help_text=_('Описание категории')
    )
    order = models.IntegerField(
        _('Порядок'),
        default=0,
        help_text=_('Порядок отображения')
    )
    
    class Meta:
        verbose_name = _('Категория проекта')
        verbose_name_plural = _('Категории проектов')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class Project(BaseModel):
    """
    Portfolio project model.
    """
    
    title = models.CharField(
        _('Название проекта'),
        max_length=200,
        help_text=_('Название проекта')
    )
    slug = models.SlugField(
        _('URL-адрес'),
        max_length=200,
        unique=True,
        help_text=_('Уникальный URL-адрес проекта')
    )
    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        verbose_name=_('Категория'),
        help_text=_('Категория проекта')
    )
    year = models.IntegerField(
        _('Год реализации'),
        help_text=_('Год реализации проекта')
    )
    area = models.DecimalField(
        _('Площадь (м²)'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Площадь объекта в квадратных метрах')
    )
    description = models.TextField(
        _('Описание'),
        help_text=_('Подробное описание проекта')
    )
    short_description = models.CharField(
        _('Краткое описание'),
        max_length=500,
        blank=True,
        help_text=_('Краткое описание для превью')
    )
    client_type = models.CharField(
        _('Тип клиента'),
        max_length=200,
        blank=True,
        help_text=_('Например: для семейной пары, для молодой семьи')
    )
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=False,
        help_text=_('Отображать проект на сайте')
    )
    is_featured = models.BooleanField(
        _('Избранное'),
        default=False,
        help_text=_('Показывать в избранных проектах')
    )
    order = models.IntegerField(
        _('Порядок'),
        default=0,
        help_text=_('Порядок отображения')
    )
    
    # SEO fields
    meta_description = models.CharField(
        _('Meta описание'),
        max_length=160,
        blank=True,
        help_text=_('Описание для поисковых систем')
    )
    meta_keywords = models.CharField(
        _('Meta ключевые слова'),
        max_length=255,
        blank=True,
        help_text=_('Ключевые слова через запятую')
    )
    
    class Meta:
        verbose_name = _('Проект')
        verbose_name_plural = _('Проекты')
        ordering = ['-is_featured', 'order', '-year', 'title']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', 'is_featured']),
            models.Index(fields=['year']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    @property
    def main_image(self):
        """
        Get the main image for the project.
        Optimized to use prefetched 'images' if available.
        """
        if hasattr(self, '_prefetched_objects_cache') and 'images' in self._prefetched_objects_cache:
            images = self._prefetched_objects_cache['images']
        else:
            images = self.images.all()
            
        # Try to find cover image first
        cover = next((img for img in images if img.is_cover), None)
        if cover:
            return cover.image
            
        # Fallback to the first image in the set
        first = next(iter(images), None)
        if first:
            return first.image
        return None

    def get_absolute_url(self):
        """Get the absolute URL for the project."""
        from django.urls import reverse
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})


class ProjectImage(BaseModel):
    """
    Images for portfolio projects.
    """
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Проект'),
        help_text=_('Проект, к которому относится изображение')
    )
    image = models.ImageField(
        _('Изображение'),
        upload_to='portfolio/%Y/%m/',
        help_text=_('Изображение проекта')
    )
    title = models.CharField(
        _('Название'),
        max_length=200,
        blank=True,
        help_text=_('Название изображения')
    )
    description = models.TextField(
        _('Описание'),
        blank=True,
        help_text=_('Описание изображения')
    )
    order = models.IntegerField(
        _('Порядок'),
        default=0,
        help_text=_('Порядок отображения в галерее')
    )
    is_cover = models.BooleanField(
        _('Обложка'),
        default=False,
        help_text=_('Использовать как обложку проекта')
    )
    
    class Meta:
        verbose_name = _('Изображение проекта')
        verbose_name_plural = _('Изображения проектов')
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.title or 'Изображение'}"


class ProjectCharacteristic(BaseModel):
    """
    Additional characteristics for projects.
    """
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='characteristics',
        verbose_name=_('Проект'),
        help_text=_('Проект')
    )
    name = models.CharField(
        _('Название'),
        max_length=100,
        help_text=_('Название характеристики')
    )
    value = models.CharField(
        _('Значение'),
        max_length=200,
        help_text=_('Значение характеристики')
    )
    order = models.IntegerField(
        _('Порядок'),
        default=0,
        help_text=_('Порядок отображения')
    )
    
    class Meta:
        verbose_name = _('Характеристика проекта')
        verbose_name_plural = _('Характеристики проектов')
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name}: {self.value}"
