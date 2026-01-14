from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel

class Sample(BaseModel):
    title = models.CharField(_('Название образца'), max_length=200)
    slug = models.SlugField(_('URL-адрес'), max_length=200, unique=True)
    year = models.IntegerField(_('Год реализации'), null=True, blank=True)
    area = models.DecimalField(_('Площадь (м²)'), max_digits=10, decimal_places=2, null=True, blank=True)
    client_type = models.CharField(_('Тип объекта/Категория'), max_length=200, blank=True)
    description = models.TextField(_('Описание'), blank=True)
    price_info = models.CharField(_('Информация о стоимости'), max_length=200, blank=True)
    pdf_file = models.FileField(_('PDF файл-пример'), upload_to='samples/pdfs/', blank=True, null=True)
    is_published = models.BooleanField(_('Опубликовано'), default=True)
    order = models.IntegerField(_('Порядок'), default=0)

    # SEO fields
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

    class Meta:
        verbose_name = _('Образец проекта')
        verbose_name_plural = _('Образцы проектов')
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    @property
    def main_image(self):
        cover = self.images.filter(is_cover=True).first()
        if cover:
            return cover.image
        first_image = self.images.first()
        if first_image:
            return first_image.image
        return None

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('samples:sample_detail', kwargs={'slug': self.slug})

class SampleImage(BaseModel):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='images', verbose_name=_('Образец'))
    image = models.ImageField(_('Изображение'), upload_to='samples/images/')
    title = models.CharField(_('Название'), max_length=200, blank=True)
    order = models.IntegerField(_('Порядок'), default=0)
    is_cover = models.BooleanField(_('Обложка'), default=False)

    class Meta:
        verbose_name = _('Изображение образца')
        verbose_name_plural = _('Изображения образцов')
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.sample.title} - {self.title or 'Изображение'}"
