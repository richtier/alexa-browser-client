from channels.routing import route

from alexa_browser_client.alexa_browser_client import consumers


channel_routing = [
    route("websocket.connect", consumers.ws_add),
    route("websocket.disconnect", consumers.ws_disconnect),
    route("websocket.receive", consumers.ws_receive),
]
