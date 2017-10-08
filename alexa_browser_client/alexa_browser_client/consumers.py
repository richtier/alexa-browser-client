from channels.generic.websockets import WebsocketConsumer

from django.conf import settings

from alexa_browser_client import AudioLifecycle

state = {
    'audio_lifecycles': {},
}


class AlexaConsumer(WebsocketConsumer):
    audio_lifecycle_class = AudioLifecycle

    def connect(self, message, **kwargs):
        super().connect(message=message, **kwargs)
        audio_lifecycle = self.create_lifecycle()
        name = self.message.reply_channel.name
        state['audio_lifecycles'][name] = audio_lifecycle
        audio_lifecycle.connect()

    def receive(self, text=None, bytes=None, **kwargs):
        name = self.message.reply_channel.name
        audio_lifecycle = state['audio_lifecycles'][name]
        audio_lifecycle.extend_audio(bytes)

    def disconnect(self, message, **kwargs):
        del state['audio_lifecycles'][self.message.reply_channel.name]

    def create_lifecycle(self):
        return self.audio_lifecycle_class(
            client_id=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID,
            secret=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET,
            refresh_token=settings.ALEXA_BROWSER_CLIENT_AVS_REFRESH_TOKEN,
            reply_channel=self.message.reply_channel,
        )
