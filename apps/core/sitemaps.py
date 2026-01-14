from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.portfolio.models import Project
from apps.samples.models import Sample
from apps.pages.models import Page

class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_published=True, is_deleted=False).exclude(slug='')

    def lastmod(self, obj):
        return obj.updated_at

class SampleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Sample.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

class PageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Page.objects.filter(is_published=True, is_deleted=False)

    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['pages:home', 'pages:about', 'pages:contacts', 'pages:sketch', 'pages:pricing', 'samples:sample_list', 'portfolio:project_list']

    def location(self, item):
        return reverse(item)
