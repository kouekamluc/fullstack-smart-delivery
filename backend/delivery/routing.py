from django.urls import path
from .consumers import LocationConsumer

websocket_urlpatterns = [
    path('ws/locations/', LocationConsumer.as_asgi()),
]
