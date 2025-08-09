from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # client will connect to ws://<host>/ws/chat/<room_name>/
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]
