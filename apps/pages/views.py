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
        
        # Portfolio data
        from apps.portfolio.models import Project, ProjectCategory
        
        # Latest 2 projects for "All" tab
        context['latest_projects'] = Project.objects.filter(
            is_published=True, 
            is_deleted=False
        ).select_related('category').prefetch_related('images')[:2]
        
        # Categories with their random/latest 2 projects
        categories = ProjectCategory.objects.filter(is_deleted=False).exclude(slug='')
        categories_with_projects = []
        
        for category in categories:
            projects = category.projects.filter(
                is_published=True, 
                is_deleted=False
            ).prefetch_related('images')[:2]
            
            if projects:
                category.home_projects = projects
                categories_with_projects.append(category)
                
        context['portfolio_categories'] = categories_with_projects
        
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
        # Add testimonials
        from .models import Testimonial
        context['testimonials'] = Testimonial.objects.filter(is_published=True)[:3]
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



class SketchView(TemplateView):
    """
    Sketch project page view.
    Displays information about sketch projects.
    """
    
    template_name = 'pages/sketch.html'
    
    def get_context_data(self, **kwargs):
        """Add context data for the sketch page."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Эскизный проект')
        context['meta_description'] = _('Стилистическая концепция интерьера')
        return context


class PricingView(TemplateView):
    """
    Pricing page view.
    Displays services and pricing information.
    """
    
    template_name = 'pages/pricing.html'
    
    def get_context_data(self, **kwargs):
        """Add context data for the pricing page."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Стоимость')
        context['meta_description'] = _('Стоимость наших услуг')
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
