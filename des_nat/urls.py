"""
URL configuration for des_nat project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Администрирование"
admin.site.site_title = "Панель управления"
admin.site.index_title = "Панель управления"

from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import ProjectSitemap, SampleSitemap, PageSitemap, StaticViewSitemap
from django.views.generic import TemplateView

sitemaps = {
    'projects': ProjectSitemap,
    'samples': SampleSitemap,
    'pages': PageSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('portfolio/', include('apps.portfolio.urls')),
    path('samples/', include('apps.samples.urls')),
    path('', include('apps.pages.urls')),
    path('leads/', include('apps.leads.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
