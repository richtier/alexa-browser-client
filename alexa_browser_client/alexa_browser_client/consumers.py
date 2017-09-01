from django.utils.module_loading import import_string

from alexa_browser_client.config import settings
from alexa_browser_client.alexa_browser_client.helpers import alexa_client


state = {
    'audio_lifecycles': {},
    'has_connected': False,
}


def conditional_connect():
    if not state['has_connected']:
        alexa_client.connect()
        state['has_connected'] = True


def ws_add(message):
    reply_channel = message.reply_channel
    reply_channel.send({'accept': True})
    lifecycle_class_path = settings.get_setting(
        'ALEXA_BROWSER_CLIENT_LIFECYCLE_CLASS'
    )
    AudioLifecycle = import_string(lifecycle_class_path)
    audio_lifecycle = AudioLifecycle(reply_channel=reply_channel)
    state['audio_lifecycles'][reply_channel.name] = audio_lifecycle
    audio_lifecycle.push_alexa_status('CONNECTING')
    conditional_connect()
    audio_lifecycle.push_alexa_status('EXPECTING_WAKEWORD')


def ws_receive(message):
    audio_lifecycle = state['audio_lifecycles'][message.reply_channel.name]
    audio_lifecycle.extend_audio(message.content['bytes'])


def ws_disconnect(message):
    del state['audio_lifecycles'][message.reply_channel.name]
