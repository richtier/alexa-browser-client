import json

from channels.generic.websockets import WebsocketConsumer

from django.conf import settings

from .helpers import AudioLifecycle

from alexa_browser_client.refreshtoken.constants import (
    SESSION_KEY_REFRESH_TOKEN
)
from .constants import AUTH_REQUIRED


class AlexaConsumer(WebsocketConsumer):
    lifecycles = {}
    audio_lifecycle_class = AudioLifecycle
    http_user_and_session = True

    @property
    def lifecycle_name(self):
        return self.message.reply_channel.name

    def connect(self, message, **kwargs):
        session = self.message.http_session
        if (session and SESSION_KEY_REFRESH_TOKEN in session):
            audio_lifecycle = self.create_lifecycle()
            self.lifecycles[self.lifecycle_name] = audio_lifecycle
            audio_lifecycle.connect()
            super().connect(message=message, **kwargs)
        else:
            self.close_auth_required()

    def close_auth_required(self):
        self.message.reply_channel.send(
            {'close': True, 'text': json.dumps({'type': AUTH_REQUIRED})},
            immediately=True
        )

    def receive(self, text=None, bytes=None, **kwargs):
        audio_lifecycle = self.lifecycles[self.lifecycle_name]
        audio_lifecycle.extend_audio(bytes)

    def disconnect(self, message, **kwargs):
        if self.lifecycle_name in self.lifecycles:
            del self.lifecycles[self.lifecycle_name]

    def create_lifecycle(self):
        return self.audio_lifecycle_class(
            client_id=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID,
            secret=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET,
            refresh_token=self.message.http_session[SESSION_KEY_REFRESH_TOKEN],
            reply_channel=self.message.reply_channel,
        )
