"""
ASGI config for mafiasi_link_shortener project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mafiasi_link_shortener.settings")
os.environ.setdefault("SHORTLINK_ENV_FILE", ".env.dev")

application = get_asgi_application()
