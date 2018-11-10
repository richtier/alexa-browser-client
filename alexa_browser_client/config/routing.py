from channels.routing import ProtocolTypeRouter
from channels.sessions import SessionMiddlewareStack

from alexa_browser_client import consumers


application = ProtocolTypeRouter({
    'websocket': SessionMiddlewareStack(consumers.AlexaConsumer)
})
