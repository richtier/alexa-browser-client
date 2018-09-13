import json

from avs_client import AlexaVoiceServiceClient
from channels.generic.websockets import WebsocketConsumer
from requests.exceptions import HTTPError

from django.conf import settings
from django.utils.functional import cached_property

from .helpers import AudioLifecycle

from alexa_browser_client.refreshtoken.constants import (
    SESSION_KEY_REFRESH_TOKEN
)
from .constants import AUTH_REQUIRED


class AuthenticationError(IOError):
    pass


class MissingRefreshToken(AuthenticationError):
    pass


class AuthenticationFailed(AuthenticationError):
    pass


class AlexaClientMixin:
    http_user_and_session = True

    alexa_client_class = AlexaVoiceServiceClient

    def handle_alexa_connect(self):
        if not self.refresh_token:
            raise MissingRefreshToken()
        else:
            try:
                self.alexa_client.connect()
            except HTTPError:
                raise AuthenticationFailed()

    @property
    def refresh_token(self):
        if not self.message.http_session:
            return None
        return self.message.http_session.get(SESSION_KEY_REFRESH_TOKEN)

    @cached_property
    def alexa_client(self):
        return self.alexa_client_class(
            client_id=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID,
            secret=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET,
            refresh_token=self.refresh_token,
        )


class LifecycleMixin:
    lifecycles = {}
    audio_lifecycle_class = AudioLifecycle

    MESSAGE_CLOSE_AUTH_REQUIRED = {
        'close': True, 'text': json.dumps({'type': AUTH_REQUIRED})
    }

    @property
    def lifecycle_name(self):
        return self.message.reply_channel.name

    def connect(self, message, **kwargs):
        audio_lifecycle = self.create_lifecycle()
        self.lifecycles[self.lifecycle_name] = audio_lifecycle
        audio_lifecycle.handle_connecting()
        try:
            self.handle_alexa_connect()
        except AuthenticationError:
            self.close_auth_required()
        else:
            audio_lifecycle.handle_connected()
            super().connect(message=message, **kwargs)

    def close_auth_required(self):
        self.message.reply_channel.send(
            self.MESSAGE_CLOSE_AUTH_REQUIRED,
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
            alexa_client=self.alexa_client,
            reply_channel=self.message.reply_channel,
        )


class AlexaConsumer(LifecycleMixin, AlexaClientMixin, WebsocketConsumer):
    pass
