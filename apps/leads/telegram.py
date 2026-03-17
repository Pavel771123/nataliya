import requests
import logging
import os
import socket
from django.conf import settings
from django.utils import timezone

# Force IPv4 for requests to avoid long delays on IPv6 fallback
import requests.packages.urllib3.util.connection as urllib3_connection

def allowed_gai_family():
    """Force IPv4 for DNS resolution"""
    return socket.AF_INET

urllib3_connection.allowed_gai_family = allowed_gai_family

logger = logging.getLogger(__name__)

class TelegramService:
    """
    Service for interacting with Telegram Bot API.
    """
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
        }
        # Optional proxy support
        self.proxies = None
        proxy_url = getattr(settings, 'TELEGRAM_PROXY', None)
        if proxy_url:
            self.proxies = {
                'http': proxy_url,
                'https': proxy_url,
            }

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
            logger.info(f"Sending Telegram message to chat {self.chat_id}... (Proxy: {'Yes' if self.proxies else 'No'})")
            
            # Connection timeout 60s, Read timeout 120s
            response = requests.post(
                url, 
                data=payload, 
                headers=self.headers, 
                proxies=self.proxies,
                timeout=(60, 120)
            )
            
            duration = (timezone.now() - start_time).total_seconds()
            response.raise_for_status()
            logger.info(f"Telegram message sent successfully in {duration:.1f}s.")
            return True
        except requests.exceptions.HTTPError as e:
            logger.error(f"Telegram API HTTP error: {e.response.status_code} - {e.response.text}")
            return False
        except requests.exceptions.Timeout:
            logger.error("Telegram request timed out.")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while sending Telegram message: {str(e)}")
            return False

    def send_document(self, file_path, caption=None, parse_mode='HTML'):
        if not self.is_configured():
            logger.warning("Telegram Bot is not configured. Missing TOKEN or CHAT_ID.")
            return False
            
        if not os.path.exists(file_path):
            logger.error(f"File not found for Telegram attachment: {file_path}")
            return False
            
        file_size = os.path.getsize(file_path)
        logger.info(f"Attempting to send document: {file_path} (Size: {file_size} bytes)")
            
        url = self.base_url + "sendDocument"
        
        try:
            with open(file_path, 'rb') as doc:
                files = {'document': doc}
                payload = {'chat_id': self.chat_id}
                if caption:
                    payload['caption'] = caption
                    payload['parse_mode'] = parse_mode
                
                start_time = timezone.now()
                logger.info(f"Sending Telegram document {file_path}... (Proxy: {'Yes' if self.proxies else 'No'})")
                
                # Connection timeout 60s, Read timeout 150s for documents
                response = requests.post(
                    url, 
                    data=payload, 
                    files=files, 
                    headers=self.headers, 
                    proxies=self.proxies,
                    timeout=(60, 150)
                )
                
                duration = (timezone.now() - start_time).total_seconds()
                response.raise_for_status()
                logger.info(f"Telegram document sent successfully in {duration:.1f}s.")
                return True
        except requests.exceptions.HTTPError as e:
            logger.error(f"Telegram API HTTP error (document): {e.response.status_code} - {e.response.text}")
            return False
        except requests.exceptions.Timeout:
            logger.error("Telegram document request timed out.")
            return False
        except (requests.exceptions.RequestException, IOError) as e:
            logger.error(f"Error sending Telegram document: {str(e)}")
            return False
