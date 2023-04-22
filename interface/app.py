import asyncio
from fastapi import FastAPI
from starlette.routing import WebSocketRoute
from starlette.routing import Route, Mount
from transport_http import http_starlette_handlers 
from transport_http import ws_starlette_handlers 
from transport_http import http_fastapi_handlers 
from transport_amqp import aiormq_handlers
from settings import static_files
from settings import DEBUG


# Add AMQP consumers 
class AppWithAMQP(FastAPI):
    def __init__(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.create_task(aiormq_handlers.consume()) 
        super().__init__(*args, **kwargs)


# Add Starlette http routes
http_starlette_routes = [
    Route('/', http_starlette_handlers.main, methods=['GET', 'POST']),   
    Route('/room/{room_name:str}', http_starlette_handlers.main, methods=['GET', 'POST']), 
    Route('/check-socket-send', http_starlette_handlers.check_socket_send, methods=['GET']), 
    Route('/check-carrot-call', http_starlette_handlers.check_carrot_call, methods=['GET']), 
]


# Add Starlette ws routes
http_starlette_routes += [
    WebSocketRoute("/room_channel", ws_starlette_handlers.ChatChannel),
]


# Add static files
http_starlette_routes += [
    Mount('/static', static_files, name='static')
]


# Make app
app = AppWithAMQP(
    debug=DEBUG, 
    routes=http_starlette_routes 
)


# Add FastApi http routes
app.include_router(http_fastapi_handlers.router) 