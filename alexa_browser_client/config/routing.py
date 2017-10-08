from channels.routing import route_class

from alexa_browser_client.alexa_browser_client import consumers


channel_routing = [
    route_class(consumers.AlexaConsumer),
]
