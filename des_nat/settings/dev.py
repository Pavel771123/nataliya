"""
Development settings for des_nat project.
"""

from .base import *

# Debug mode enabled for development
DEBUG = True

# Email backend for development (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Development-specific middleware (if needed)
# MIDDLEWARE += []

# Allow all hosts in development
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']
