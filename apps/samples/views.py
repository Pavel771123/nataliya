from django.views.generic import ListView, DetailView
from .models import Sample

class SampleListView(ListView):
    """
    View for displaying the list of project samples.
    """
    model = Sample
    template_name = 'samples/sample_list.html'
    context_object_name = 'samples'
    paginate_by = 6

    def get_queryset(self):
        return Sample.objects.filter(is_published=True).prefetch_related('images')

class SampleDetailView(DetailView):
    """
    View for displaying a single project sample.
    Replicates the portfolio detail logic.
    """
    model = Sample
    template_name = 'samples/sample_detail.html'
    context_object_name = 'project'  # Reusing 'project' to match portfolio templates
