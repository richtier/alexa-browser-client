import json
import threading

from alexa_client import AlexaClient
from channels.generic.websocket import WebsocketConsumer
from requests.exceptions import HTTPError

from django.conf import settings

from alexa_browser_client import constants, helpers


class AuthenticationError(IOError):
    pass


class MissingRefreshToken(AuthenticationError):
    pass


class AuthenticationFailed(AuthenticationError):
    pass


class AlexaClientMixin:

    alexa_client_class = AlexaClient

    def connect(self):
        super().connect()
        self.send_status(constants.CONNECTING)
        self.alexa_client = self.alexa_client_class(
            client_id=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID,
            secret=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET,
            refresh_token=self.refresh_token,
        )
        try:
            self.handle_alexa_connect()
        except AuthenticationError:
            self.close(code=3000)

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
        if not self.scope['session']:
            return None
        return self.scope['session'].get(constants.SESSION_KEY_REFRESH_TOKEN)

    def disconnect(self, *args, **kwargs):
        self.alexa_client.ping_manager.cancel()
        return super().disconnect(*args, **kwargs)


class LifecycleMixin:
    audio_lifecycle_class = helpers.AudioLifecycle

    def connect(self):
        super().connect()
        self.send_status(constants.EXPECTING_WAKEWORD)
        self.audio_lifecycle = self.audio_lifecycle_class(
            on_command_started=self.handle_command_started,
            on_command_finished=self.handle_command_finished,
        )

    def receive(self, text_data=None, bytes_data=None):
        super().receive(text_data=text_data, bytes_data=bytes_data)
        self.audio_lifecycle.extend_audio(bytes_data)

    def handle_command_started(self):
        self.send_status(constants.EXPECTING_COMMAND)

    def handle_command_finished(self):
        self.send_status(constants.EXPECTING_WAKEWORD)


class AlexaConsumer(LifecycleMixin, AlexaClientMixin, WebsocketConsumer):

    dialog_request_id = None

    def receive(self, text_data=None, bytes_data=None):
        if text_data == 'ExpectSpeech':
            self.audio_lifecycle.handle_command_started(None)
        else:
            super().receive(text_data=text_data, bytes_data=bytes_data)

    def send_status(self, message_id):
        self.send(text_data=json.dumps({'type': message_id}))

    def handle_command_started(self, wakeword_name):
        super().handle_command_started()
        thr = threading.Thread(target=self.send_command_to_avs)
        thr.start()

    def send_command_to_avs(self):
        directives = self.alexa_client.send_audio_file(
            self.audio_lifecycle.as_file,
            dialog_request_id=self.dialog_request_id
        )
        self.dialog_request_id = None
        for directive in (directives or []):
            if directive.name == 'ExpectSpeech':
                headers = directive.directive['header']
                self.dialog_request_id = headers['dialogRequestId']
                self.send_status('ExpectSpeech')
            if directive.name in ['Speak', 'Play']:
                self.send(bytes_data=directive.audio_attachment)
        else:
            self.send_status(constants.EXPECTING_WAKEWORD)
