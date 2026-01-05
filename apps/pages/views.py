"""
Pages views module.
Contains views for static pages.
"""

from django.views.generic import TemplateView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Page


class HomeView(TemplateView):
    """
    Home page view.
    Displays the main landing page.
    """
    
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        """Add context data for the home page."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Главная')
        context['meta_description'] = _('Добро пожаловать на наш сайт')
        return context


class AboutView(TemplateView):
    """
    About page view.
    Displays information about the company/person.
    """
    
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        """Add context data for the about page."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('О нас')
        context['meta_description'] = _('Информация о компании')
        return context


class ContactsView(TemplateView):
    """
    Contacts page view.
    Displays contact information.
    """
    
    template_name = 'pages/contacts.html'
    
    def get_context_data(self, **kwargs):
        """Add context data for the contacts page."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Контакты')
        context['meta_description'] = _('Свяжитесь с нами')
        return context


class PageDetailView(DetailView):
    """
    Dynamic page detail view.
    Displays pages from the database.
    """
    
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'
    
    def get_queryset(self):
        """Only show published, non-deleted pages."""
        return Page.objects.filter(
            is_published=True,
            is_deleted=False
        )
    
    def get_context_data(self, **kwargs):
        """Add context data for the page."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context['meta_description'] = self.object.meta_description or self.object.title
        return context
