from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r'^ws/comments/(?P<post_id>\d+)/$', consumer.CommentConsumer.as_asgi()),
]
