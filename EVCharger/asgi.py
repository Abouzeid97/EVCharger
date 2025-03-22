"""
ASGI config for EVCharger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import OcppApp.websockets.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EVCharger.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(OcppApp.websockets.routing.websocket_urlpatterns),
    }
)