from collections import OrderedDict
import json

from avs_client import AlexaVoiceServiceClient
import command_lifecycle

from django.conf import settings


class AudioLifecycle(command_lifecycle.BaseAudioLifecycle):
    audio_converter_class = command_lifecycle.helpers.WebAudioToWavConverter
    alexa_client_class = AlexaVoiceServiceClient

    def __init__(self, reply_channel):
        self.reply_channel = reply_channel
        self.alexa_client = self.alexa_client_class(
            client_id=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID,
            secret=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET,
            refresh_token=settings.ALEXA_BROWSER_CLIENT_AVS_REFRESH_TOKEN,
        )
        super().__init__()

    def extend_audio(self, *args, **kwargs):
        super().extend_audio(*args, **kwargs)
        self.alexa_client.conditional_ping()

    def handle_command_started(self):
        self.push_alexa_status('EXPECTING_COMMAND')
        super().handle_command_started()
        self.send_command_to_avs()

    def handle_command_finised(self):
        self.push_alexa_status('EXPECTING_WAKEWORD')
        super().handle_command_finised()

    def send_command_to_avs(self, context=None):
        audio_file = command_lifecycle.helpers.LifeCycleFileLike(self)
        alexa_response_audio = self.alexa_client.send_audio_file(
            audio_file=audio_file, context=context
        )
        if alexa_response_audio:
            self.reply_channel.send({'bytes': alexa_response_audio})

    def push_alexa_status(self, message_id):
        message = json.dumps(OrderedDict([('type', message_id)]))
        self.reply_channel.send({'text': message}, immediately=True)
