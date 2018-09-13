import json

import command_lifecycle

from . import constants


class AudioLifecycle(command_lifecycle.BaseAudioLifecycle):
    audio_converter_class = command_lifecycle.helpers.WebAudioToWavConverter
    filelike_wrapper_class = command_lifecycle.helpers.LifeCycleFileLike

    def __init__(self, alexa_client, reply_channel):
        self.reply_channel = reply_channel
        self.alexa_client = alexa_client
        super().__init__()

    def handle_connecting(self):
        self.push_alexa_status(constants.CONNECTING)

    def handle_connected(self):
        self.push_alexa_status(constants.EXPECTING_WAKEWORD)

    def extend_audio(self, *args, **kwargs):
        super().extend_audio(*args, **kwargs)
        self.alexa_client.conditional_ping()

    def handle_command_started(self):
        self.push_alexa_status(constants.EXPECTING_COMMAND)
        super().handle_command_started()
        self.send_command_to_avs()

    def handle_command_finised(self):
        self.push_alexa_status(constants.EXPECTING_WAKEWORD)
        super().handle_command_finised()

    def send_command_to_avs(self):
        alexa_response_audio = self.alexa_client.send_audio_file(
            audio_file=self.filelike_wrapper_class(self)
        )
        if alexa_response_audio:
            self.reply_channel.send({'bytes': alexa_response_audio})

    def push_alexa_status(self, message_id):
        self.reply_channel.send(
            {'text': json.dumps({'type': message_id})},
            immediately=True
        )
