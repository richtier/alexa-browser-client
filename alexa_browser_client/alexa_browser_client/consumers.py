from alexa_browser_client.alexa_browser_client import helpers


audio_lifecycles = {}


def ws_add(message):
    reply_channel = message.reply_channel
    audio_lifecycle = helpers.AudioLifecycle(reply_channel=reply_channel)
    audio_lifecycles[reply_channel.name] = audio_lifecycle
    reply_channel.send({'accept': True})


def ws_receive(message):
    audio_lifecycle = audio_lifecycles[message.reply_channel.name]
    audio_lifecycle.extend_audio(message.content['bytes'])


def ws_disconnect(message):
    del audio_lifecycles[message.reply_channel.name]
