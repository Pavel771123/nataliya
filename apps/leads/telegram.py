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
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending Telegram message: {e}")
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
                
                response = requests.post(url, data=payload, files=files, timeout=20)
                response.raise_for_status()
                return True
        except (requests.exceptions.RequestException, IOError) as e:
            logger.error(f"Error sending Telegram document: {e}")
            return False
