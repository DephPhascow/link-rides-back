import os

from main.graphql.MyGraphQL import MyGraphQL
from django.core.asgi import get_asgi_application
from starlette.websockets import WebSocketDisconnect


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back.settings')

from main.graphql.scheme import schema

django_application = get_asgi_application()

async def application(scope, receive, send):
    if scope["type"] == "http":
        await django_application(scope, receive, send)
    elif scope["type"] == "websocket":
        try:
            from main.graphql.scheme import schema

            graphql_app = MyGraphQL(schema, keep_alive=True, keep_alive_interval=5)

            await graphql_app(scope, receive, send)
        except WebSocketDisconnect:
            pass
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")