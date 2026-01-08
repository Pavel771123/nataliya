"""
Portfolio views module.
"""

from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _
from .models import Project, ProjectCategory


class ProjectListView(ListView):
    """
    List view for portfolio projects.
    """
    
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        """Only show published, non-deleted projects."""
        queryset = Project.objects.filter(
            is_published=True,
            is_deleted=False
        ).exclude(slug='').select_related('category').prefetch_related('images')
        
        # Filter by category if provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add context data."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Портфолио')
        context['categories'] = ProjectCategory.objects.filter(
            is_deleted=False
        ).exclude(slug='').order_by('order', 'name')
        
        # Add current category if filtering
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            try:
                context['current_category'] = ProjectCategory.objects.get(slug=category_slug)
            except ProjectCategory.DoesNotExist:
                pass
        
        return context


class ProjectDetailView(DetailView):
    """
    Detail view for portfolio project.
    """
    
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        """Only show published, non-deleted projects."""
        return Project.objects.filter(
            is_published=True,
            is_deleted=False
        ).select_related('category').prefetch_related(
            'images',
            'characteristics'
        )
    
    def get_context_data(self, **kwargs):
        """Add context data."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        context['meta_description'] = self.object.meta_description or self.object.short_description
        
        # Get related projects
        context['related_projects'] = Project.objects.filter(
            is_published=True,
            is_deleted=False,
            category=self.object.category
        ).exclude(slug='').exclude(id=self.object.id)[:3]
        
        return context
