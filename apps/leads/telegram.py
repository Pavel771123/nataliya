import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class TelegramService:
    """
    Service for interacting with Telegram Bot API.
    """
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    def is_configured(self):
        return bool(self.token and self.chat_id)

    def send_message(self, text, parse_mode='HTML'):
        if not self.is_configured():
            logger.warning("Telegram Bot is not configured. Missing TOKEN or CHAT_ID.")
            return False
            
        url = self.base_url + "sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': parse_mode
        }
        
        try:
            start_time = timezone.now()
            logger.info(f"Sending Telegram message to chat {self.chat_id}...")
            response = requests.post(url, data=payload, timeout=90)
            duration = (timezone.now() - start_time).total_seconds()
            response.raise_for_status()
            logger.info(f"Telegram message sent successfully in {duration:.1f}s.")
            return True
        except requests.exceptions.HTTPError as e:
            logger.error(f"Telegram API HTTP error: {e.response.status_code} - {e.response.text}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while sending Telegram message: {str(e)}")
            return False

    def send_document(self, file_path, caption=None, parse_mode='HTML'):
        if not self.is_configured():
            logger.warning("Telegram Bot is not configured. Missing TOKEN or CHAT_ID.")
            return False
            
        url = self.base_url + "sendDocument"
        
        try:
            with open(file_path, 'rb') as doc:
                files = {'document': doc}
                payload = {'chat_id': self.chat_id}
                if caption:
                    payload['caption'] = caption
                    payload['parse_mode'] = parse_mode
                
                start_time = timezone.now()
                logger.info(f"Sending Telegram document {file_path} to chat {self.chat_id}...")
                response = requests.post(url, data=payload, files=files, timeout=120)
                duration = (timezone.now() - start_time).total_seconds()
                response.raise_for_status()
                logger.info(f"Telegram document sent successfully in {duration:.1f}s.")
                return True
        except requests.exceptions.HTTPError as e:
            logger.error(f"Telegram API HTTP error (document): {e.response.status_code} - {e.response.text}")
            return False
        except (requests.exceptions.RequestException, IOError) as e:
            logger.error(f"Error sending Telegram document: {str(e)}")
            return False
