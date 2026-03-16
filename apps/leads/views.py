from django.views.generic import CreateView
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Lead
from .forms import LeadForm

from .telegram import TelegramService
from django.utils.html import escape
from django.utils import timezone
import threading

class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'pages/contacts.html'
    
    def form_valid(self, form):
        self.object = form.save()
        
        # Send notifications in background to prevent 10s wait
        threading.Thread(target=self.send_email_notification, args=(self.object,)).start()
        threading.Thread(target=self.send_telegram_notification, args=(self.object,)).start()
        
        # Return success partial
        return render(self.request, 'leads/partials/success.html')
    
    def form_invalid(self, form):
        # We need to return the form with errors.
        # Since this is HTMX, returning the full page isn't what we want inside the swap target.
        # For simplicity, if it's HTMX, we can just render the form part again.
        # However, we don't have a partial for the form itself. 
        # For now, return a simple error message to the hx-target.
        return render(self.request, 'leads/partials/error.html', {'form': form}, status=400)

    def send_email_notification(self, lead):
        try:
            subject = f"Новая заявка с сайта: {lead.name}"
            body = f"""
            Имя: {lead.name}
            Телефон: {lead.phone}
            Описание: {lead.description or 'Не указано'}
            """
            
            recipient_list = [settings.DEFAULT_FROM_EMAIL] if hasattr(settings, 'DEFAULT_FROM_EMAIL') else ['info@example.com']
            
            email = EmailMessage(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
                recipient_list,
            )
            
            if lead.file:
                email.attach_file(lead.file.path)
                
            email.send(fail_silently=True)
        except Exception:
            # Silence email errors to not break lead submission
            pass

    def send_telegram_notification(self, lead):
        try:
            telegram = TelegramService()
            if not telegram.is_configured():
                return

            # Format fields (escaping for HTML safety)
            name = escape(lead.name or "—")
            phone = escape(lead.phone or "—")
            description = escape(lead.description or "—")
            file_status = "прикреплён" if lead.file else "отсутствует"
            datetime = timezone.localtime(lead.created_at).strftime("%d.%m.%Y %H:%M")
            page_url = escape(self.request.META.get('HTTP_REFERER', "—"))

            message = (
                f"📩 <b>Новая заявка с сайта</b>\n\n"
                f"👤 <b>Имя:</b> {name}\n"
                f"📞 <b>Телефон:</b> {phone}\n"
                f"📝 <b>Описание:</b>\n{description}\n\n"
                f"📎 <b>Файл:</b> {file_status}\n"
                f"🕒 <b>Дата:</b> {datetime}\n"
                f"🌐 <b>Страница:</b> {page_url}"
            )

            # Send message
            telegram.send_message(message)

            # Send document if exists
            if lead.file:
                caption = f"📎 Файл к заявке от {name} ({phone})"
                telegram.send_document(lead.file.path, caption=caption)
        except Exception:
            # Silence telegram errors to not break lead submission
            pass
