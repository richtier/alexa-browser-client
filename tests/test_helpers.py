from unittest import mock

import command_lifecycle
import pytest

from alexa_browser_client import helpers


@pytest.fixture
def handle_command_started():
    return mock.Mock()


@pytest.fixture
def handle_command_finised():
    return mock.Mock()


@pytest.fixture
def lifecycle(handle_command_started, handle_command_finised):
    class TestAudioLifecycle(helpers.AudioLifecycle):
        audio_detector_class = mock.Mock()
        filelike_wrapper_class = mock.Mock()

    return TestAudioLifecycle(
        on_command_started=handle_command_started,
        on_command_finished=handle_command_finised,
    )


def test_audio_lifecycle_audio_detector_class():
    assert helpers.AudioLifecycle.audio_converter_class == (
        command_lifecycle.helpers.WebAudioToWavConverter
    )


def test_audio_lifecycle_handle_command_started(
    lifecycle, handle_command_started
):
    lifecycle.audio_detector.get_uttered_wakeword_name.return_value = 'ALEXA'

    assert handle_command_started.call_count == 0
    lifecycle.handle_command_started()
    assert handle_command_started.call_count == 1
    assert handle_command_started.call_args == mock.call(wakeword_name='ALEXA')


def test_audio_lifecycle_handle_command_finised(
    lifecycle, handle_command_finised
):
    assert handle_command_finised.call_count == 0
    lifecycle.handle_command_finised()
    assert handle_command_finised.call_count == 1


def test_as_file(lifecycle):
    lifecycle.as_file

    assert lifecycle.filelike_wrapper_class.call_count == 1
    assert lifecycle.filelike_wrapper_class.call_args == mock.call(lifecycle)
