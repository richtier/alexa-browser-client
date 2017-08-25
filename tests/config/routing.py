from channels.routing import include


channel_routing = [
    include(
        'alexa_browser_client.config.routing.channel_routing'
    )
]
