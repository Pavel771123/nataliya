"""
Pages models module.
Contains models for managing static pages.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class Page(BaseModel):
    """
    Model for managing static pages.
    """
    
    title = models.CharField(
        _('Заголовок'),
        max_length=200,
        help_text=_('Заголовок страницы')
    )
    slug = models.SlugField(
        _('URL-адрес'),
        max_length=200,
        unique=True,
        help_text=_('Уникальный URL-адрес страницы')
    )
    content = models.TextField(
        _('Содержимое'),
        help_text=_('Основное содержимое страницы')
    )
    meta_description = models.CharField(
        _('Meta описание'),
        max_length=160,
        blank=True,
        help_text=_('Описание для поисковых систем (до 160 символов)')
    )
    meta_keywords = models.CharField(
        _('Meta ключевые слова'),
        max_length=255,
        blank=True,
        help_text=_('Ключевые слова через запятую')
    )
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=False,
        help_text=_('Отображать страницу на сайте')
    )
    order = models.IntegerField(
        _('Порядок'),
        default=0,
        help_text=_('Порядок отображения в меню')
    )
    
    class Meta:
        verbose_name = _('Страница')
        verbose_name_plural = _('Страницы')
        ordering = ['order', 'title']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', 'order']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Get the absolute URL for the page."""
        from django.urls import reverse
        return reverse('pages:page_detail', kwargs={'slug': self.slug})

class Testimonial(BaseModel):
    """
    Client testimonial model.
    """
    
    client_name = models.CharField(
        _('Имя клиента'),
        max_length=100,
        help_text=_('Имя клиента')
    )
    client_info = models.CharField(
        _('Информация о проекте'),
        max_length=200,
        blank=True,
        help_text=_('Например: ЖК Символ, 100 м²')
    )
    text = models.TextField(
        _('Текст отзыва'),
        help_text=_('Текст отзыва')
    )
    rating = models.IntegerField(
        _('Оценка'),
        default=5,
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text=_('Оценка от 1 до 5')
    )
    is_published = models.BooleanField(
        _('Опубликовано'),
        default=True,
        help_text=_('Отображать отзыв на сайте')
    )
    order = models.IntegerField(
        _('Порядок'),
        default=0,
        help_text=_('Порядок отображения')
    )
    
    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.client_name} ({self.rating}★)"
