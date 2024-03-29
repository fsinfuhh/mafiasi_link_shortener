"""
WSGI config for mafiasi_link_shortener project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mafiasi_link_shortener.settings")
os.environ.setdefault("SHORTLINK_ENV_FILE", ".env.dev")

application = get_wsgi_application()
