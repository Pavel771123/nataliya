"""
Development settings for des_nat project.
"""

from .base import *

# Debug MUST be True during local development to serve static files (CSS, JS, Images)
DEBUG = True
# Email backend for development (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development-specific middleware (if needed)

INTERNAL_IPS = ['127.0.0.1']

# Allow all hosts in development
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']
