import logging
import threading
from django.views.generic import CreateView
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.html import escape
from django.utils import timezone
from .models import Lead
from .forms import LeadForm
from .telegram import TelegramService

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
        
        # Send notifications in background to prevent 10s wait
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
        self.send_telegram_notification(lead, referer)

    def send_telegram_notification(self, lead, referer):
        try:
            telegram = TelegramService()
            if not telegram.is_configured():
                logger.warning("Telegram not configured (missing tokens)")
                return

            # Format fields
            name = escape(lead.name or "—")
            phone = escape(lead.phone or "—")
            description = escape(lead.description or "—")
            file_status = "прикреплён" if lead.file else "отсутствует"
            dt_str = timezone.localtime(lead.created_at).strftime("%d.%m.%Y %H:%M")
            page_url = escape(referer)

            message = (
                f"📩 <b>Новая заявка с сайта</b>\n\n"
                f"👤 <b>Имя:</b> {name}\n"
                f"📞 <b>Телефон:</b> {phone}\n"
                f"📝 <b>Описание:</b>\n{description}\n\n"
                f"📎 <b>Файл:</b> {file_status}\n"
                f"🕒 <b>Дата:</b> {dt_str}\n"
                f"🌐 <b>Страница:</b> {page_url}"
            )

            # Send message
            success = telegram.send_message(message)
            if success:
                logger.info(f"Telegram message sent for lead {lead.id}")
            else:
                logger.error(f"Telegram message failed for lead {lead.id}")

            # Send document if exists
            if lead.file and success:
                caption = f"📎 Файл к заявке от {name} ({phone})"
                telegram.send_document(lead.file.path, caption=caption)
        except Exception as e:
            logger.exception(f"Critical error in Telegram notification thread for lead {lead.id}: {str(e)}")
