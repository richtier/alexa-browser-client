from django.utils.module_loading import import_string

from alexa_browser_client.config import settings

audio_lifecycles = {}


def ws_add(message):
    lifecycle_class_path = settings.get_setting(
        'ALEXA_BROWSER_CLIENT_LIFECYCLE_CLASS'
    )
    AudioLifecycle = import_string(lifecycle_class_path)
    reply_channel = message.reply_channel
    audio_lifecycle = AudioLifecycle(reply_channel=reply_channel)
    audio_lifecycles[reply_channel.name] = audio_lifecycle
    reply_channel.send({'accept': True})


def ws_receive(message):
    audio_lifecycle = audio_lifecycles[message.reply_channel.name]
    audio_lifecycle.extend_audio(message.content['bytes'])


def ws_disconnect(message):
    del audio_lifecycles[message.reply_channel.name]
