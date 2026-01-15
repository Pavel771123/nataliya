from django.views.generic import CreateView
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Lead
from .forms import LeadForm

from .telegram import TelegramService
from django.utils import timezone

class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/form.html'  # Fallback
    
    def form_valid(self, form):
        self.object = form.save()
        
        # Send notifications
        self.send_email_notification(self.object)
        self.send_telegram_notification(self.object)
        
        # Return success partial
        return render(self.request, 'leads/partials/success.html')
    
    def form_invalid(self, form):
        return super().form_invalid(form)

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

            # Format fields
            name = lead.name or "—"
            phone = lead.phone or "—"
            description = lead.description or "—"
            file_status = "прикреплён" if lead.file else "отсутствует"
            datetime = timezone.localtime(lead.created_at).strftime("%d.%m.%Y %H:%M")
            page_url = self.request.META.get('HTTP_REFERER', "—")

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
