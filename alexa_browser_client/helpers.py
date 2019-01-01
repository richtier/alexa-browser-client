import command_lifecycle


class AudioLifecycle(command_lifecycle.BaseAudioLifecycle):
    audio_converter_class = command_lifecycle.helpers.WebAudioToWavConverter
    filelike_wrapper_class = command_lifecycle.helpers.LifeCycleFileLike

    def __init__(
        self, on_command_started, on_command_finished, *args, **kwargs
    ):
        self.on_command_started = on_command_started
        self.on_command_finished = on_command_finished
        super().__init__(*args, **kwargs)

    @property
    def as_file(self):
        return self.filelike_wrapper_class(self)

    def handle_command_started(self, wakeword_name):
        super().handle_command_started(wakeword_name=wakeword_name)
        self.on_command_started(wakeword_name=wakeword_name)

    def handle_command_finised(self):
        super().handle_command_finised()
        self.on_command_finished()
