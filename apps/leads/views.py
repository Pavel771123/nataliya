from django.views.generic import CreateView
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Lead
from .forms import LeadForm

class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/form.html'  # Fallback
    
    def form_valid(self, form):
        self.object = form.save()
        
        # Send email
        self.send_email_notification(self.object)
        
        # Return success partial
        return render(self.request, 'leads/partials/success.html')
    
    def form_invalid(self, form):
        # Return form with errors (rendered as partial if needed, but for now just basic support)
        # Implementing a simple response with error status for HTMX handling might be better,
        # but the user requested 'Success message without reload'. 
        return super().form_invalid(form)

    def send_email_notification(self, lead):
        subject = f"Новая заявка с сайта: {lead.name}"
        body = f"""
        Имя: {lead.name}
        Телефон: {lead.phone}
        Описание: {lead.description or 'Не указано'}
        """
        
        # Use settings for admin email, or a placeholder
        recipient_list = [settings.DEFAULT_FROM_EMAIL] if hasattr(settings, 'DEFAULT_FROM_EMAIL') else ['info@example.com']
        
        email = EmailMessage(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
            recipient_list,
        )
        
        if lead.file:
            email.attach_file(lead.file.path)
            
        email.send(fail_silently=False)
