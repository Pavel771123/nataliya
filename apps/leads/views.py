import logging
import threading
from decouple import config
from django.views.generic import CreateView
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import escape
from django.utils import timezone
from .models import Lead
from .forms import LeadForm

logger = logging.getLogger(__name__)

class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'pages/contacts.html'
    
    def form_valid(self, form):
        self.object = form.save()
        
        # Capture critical request data BEFORE starting the thread
        # accessing self.request in a thread after response is sent can crash
        referer = self.request.META.get('HTTP_REFERER', "—")
        
        # Send notifications in background to prevent wait times
        threading.Thread(
            target=self.send_notifications_task, 
            args=(self.object, referer)
        ).start()
        
        # Return success partial
        return render(self.request, 'leads/partials/success.html')
    
    def form_invalid(self, form):
        return render(self.request, 'leads/partials/error.html', {'form': form}, status=400)

    def send_notifications_task(self, lead, referer):
        """Wrapper task to run in a thread"""
        self.send_email_notification(lead, referer)

    def send_email_notification(self, lead, referer):
        try:
            admin_email = config('ADMIN_EMAIL', default=None)
            if not admin_email:
                logger.warning("ADMIN_EMAIL is not configured, skipping email notification.")
                return

            dt_str = timezone.localtime(lead.created_at).strftime("%d.%m.%Y %H:%M")
            subject = f"Новая заявка: {lead.name} ({dt_str})"
            
            body = (
                f"📩 Новая заявка с сайта\n\n"
                f"👤 Имя: {lead.name or '—'}\n"
                f"📞 Телефон: {lead.phone or '—'}\n"
                f"📝 Описание:\n{lead.description or '—'}\n\n"
                f"🕒 Дата: {dt_str}\n"
                f"🌐 Страница: {referer or '—'}"
            )

            email = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
            )

            if lead.file:
                email.attach_file(lead.file.path)

            email.send(fail_silently=False)
            logger.info(f"Email notification sent successfully for lead {lead.id}")
        except Exception as e:
            logger.exception(f"Error sending email notification for lead {lead.id}: {str(e)}")