from channels.routing import include


channel_routing = [
    include(
        'alexa_browser_client.alexa_browser_client.routing.channel_routing'
    )
]
