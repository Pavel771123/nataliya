"""
Core utilities module.
Contains helper functions and utilities.
"""

import re
from typing import Optional
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(phone: str) -> bool:
    """
    Validate phone number format.
    Accepts various formats: +7XXXXXXXXXX, 8XXXXXXXXXX, etc.
    """
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Check if it matches Russian phone number patterns
    patterns = [
        r'^\+7\d{10}$',  # +7XXXXXXXXXX
        r'^8\d{10}$',     # 8XXXXXXXXXX
        r'^7\d{10}$',     # 7XXXXXXXXXX
    ]
    
    return any(re.match(pattern, cleaned) for pattern in patterns)


def validate_email_format(email: str) -> bool:
    """
    Validate email format using regex.
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def send_notification_email(
    subject: str,
    message: str,
    recipient_list: list,
    from_email: Optional[str] = None,
    fail_silently: bool = False
) -> int:
    """
    Send notification email.
    
    Args:
        subject: Email subject
        message: Email message body
        recipient_list: List of recipient email addresses
        from_email: Sender email (defaults to DEFAULT_FROM_EMAIL)
        fail_silently: If True, don't raise exceptions on errors
    
    Returns:
        Number of successfully sent emails
    """
    if from_email is None:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
    
    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently
    )


def sanitize_html(text: str) -> str:
    """
    Remove HTML tags from text for security.
    Simple implementation - for production consider using bleach library.
    """
    return re.sub(r'<[^>]+>', '', text)


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].rstrip() + suffix


def get_client_ip(request) -> str:
    """
    Get client IP address from request.
    Handles proxy headers.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RateLimiter:
    """
    Simple rate limiter for preventing spam.
    For production, consider using django-ratelimit or Redis-based solution.
    """
    
    def __init__(self, max_requests: int = 5, time_window: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum number of requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed.
        
        Args:
            identifier: Unique identifier (e.g., IP address, user ID)
        
        Returns:
            True if allowed, False otherwise
        """
        from datetime import datetime, timedelta
        
        now = datetime.now()
        
        # Clean old entries
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if now - req_time < timedelta(seconds=self.time_window)
            ]
        else:
            self.requests[identifier] = []
        
        # Check if limit exceeded
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[identifier].append(now)
        return True
