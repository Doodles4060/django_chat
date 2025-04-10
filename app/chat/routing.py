from django.urls import path, re_path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    # path("ws/socket-server/", ChatConsumer.as_asgi()),
    re_path(r'ws/chat/groups/(?P<pk>\d+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/groups/(?P<group_name>\w+)/$', ChatConsumer.as_asgi())
]