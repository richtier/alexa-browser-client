from collections import OrderedDict
import json

from avs_client.avs_client.client import AlexaVoiceServiceClient
import command_lifecycle
from django.conf import settings


class LifeCycleFileLike:
    def __init__(self, audio_lifecycle):
        self.audio_lifecycle = audio_lifecycle

    def read(self, size):
        return self.audio_lifecycle.audio_buffer.popleft_size(size)

    def __len__(self):
        # when length == 0 the uploader will close the request. If the stream
        # has all the data popped from it, but there is more to be written to
        # it then make the uploader wait by making the uploader think there is
        # data available.
        if self.audio_lifecycle.is_command_pending:
            return 1025
        return len(self.audio_lifecycle.audio_buffer)


class AudioLifecycle(command_lifecycle.BaseAudioLifecycle):
    audio_converter = command_lifecycle.helpers.WebAudioToWavConverter
    alexa_client = AlexaVoiceServiceClient(
        client_id=settings.ALEXA_VOICE_SERVICE_CLIENT_ID,
        secret=settings.ALEXA_VOICE_SERVICE_CLIENT_SECRET,
        refresh_token=settings.ALEXA_VOICE_SERVICE_REFRESH_TOKEN,
    )

    def __init__(self, reply_channel):
        self.reply_channel = reply_channel
        self.alexa_client.connect()
        super().__init__()

    def extend_audio(self, wav_bytes):
        super().extend_audio(wav_bytes)
        if self.alexa_client.should_ping():
            self.alexa_client.ping()

    def handle_command_started(self):
        message = json.dumps(
            OrderedDict([('type', 'EXPECTING_COMMAND'), ('payload', True)])
        )
        self.reply_channel.send({'text': message}, immediately=True)
        super().handle_command_started()
        self.send_command_to_avs()

    def handle_command_finised(self):
        message = json.dumps(
            OrderedDict([('type', 'EXPECTING_COMMAND'), ('payload', False)])
        )
        self.reply_channel.send({'text': message})
        super().handle_command_finised()

    def send_command_to_avs(self):
        audio_file = LifeCycleFileLike(self)
        alexa_response_audio = self.alexa_client.send_audio_file(audio_file)
        if alexa_response_audio:
            self.reply_channel.send({'bytes': alexa_response_audio})
