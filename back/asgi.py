import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from strawberry.channels import GraphQLHTTPConsumer, GraphQLWSConsumer
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')
http = get_asgi_application()

from main.graphql.scheme import schema

from gqlauth.core.middlewares import channels_jwt_middleware
# from main.websoket import websocket_urlpattern
# from main.consumers import AVideoChatConnectConsumer, CConsumer
import logging

logger = logging.getLogger(__name__)
logger.debug("are see me?")
print("are see me? console")

graphq_websocket_urlpatterns = [
    re_path("^graphql", channels_jwt_middleware(GraphQLWSConsumer.as_asgi(schema=schema))),
    # re_path('^ws/chat/video/(?P<room_name>\w+)/$', AVideoChatConnectConsumer.as_asgi()),
    # re_path('^ws/chat/c/(?P<room_name>\w+)/$', CConsumer.as_asgi())
]
gql_http_consumer = AuthMiddlewareStack(
    channels_jwt_middleware(GraphQLHTTPConsumer.as_asgi(schema=schema))
)

application = ProtocolTypeRouter(
    {
        "http": URLRouter(
            [
                re_path("^graphql", gql_http_consumer),
                re_path("^", http),
            ]
        ),
        "websocket": AuthMiddlewareStack(URLRouter(graphq_websocket_urlpatterns)),
        # "websocket": URLRouter([
        #     re_path(r'^ws/chat/video/(?P<room_name>\w+)/$', AVideoChatConnectConsumer.as_asgi())    
        # ]),
    }
)
