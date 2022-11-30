"""
ASGI config for mafiasi_link_shortener project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

# this does not currently exist but we import it to intentionally throw an error
from configurations.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mafiasi_link_shortener.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

application = get_asgi_application()
