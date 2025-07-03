"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named `application.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

from dotenv import load_dotenv

load_dotenv()
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

django.setup()

from apps.blog.routing import websocket_urlpatterns

django_asgi_app = get_asgi_application()

# <-- And this one


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
