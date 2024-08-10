import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import delivery.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_logistics.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            delivery.routing.websocket_urlpatterns
        )
    ),
})
