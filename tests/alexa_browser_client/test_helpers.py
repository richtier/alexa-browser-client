import pytest
from unittest.mock import call, patch, Mock

from alexa_browser_client.alexa_browser_client import helpers
import command_lifecycle


@pytest.fixture(autouse=True)
def mock_client_send_audio_file(request):
    stub = patch('avs_client.AlexaVoiceServiceClient.send_audio_file')
    yield stub.start()
    stub.stop()


@pytest.fixture(autouse=True)
def mock_client_send_conditional_ping(request):
    stub = patch('avs_client.AlexaVoiceServiceClient.conditional_ping')
    yield stub.start()
    stub.stop()


@pytest.fixture
def reply_channel():
    return Mock()


@pytest.fixture
def lifecycle(reply_channel, settings):
    class TestAudioLifecycle(helpers.AudioLifecycle):
        audio_detector_class = Mock()
    return TestAudioLifecycle(
        reply_channel=reply_channel,
        client_id=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID,
        secret=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET,
        refresh_token=settings.ALEXA_BROWSER_CLIENT_AVS_REFRESH_TOKEN,
    )


def test_audio_lifecycle_audio_detector_class():
    assert helpers.AudioLifecycle.audio_converter_class == (
        command_lifecycle.helpers.WebAudioToWavConverter
    )


def test_audio_lifecycle_sets_attributes(lifecycle, reply_channel):
    authenticator = lifecycle.alexa_client.authentication_manager

    assert lifecycle.reply_channel == reply_channel
    assert authenticator.client_id == 'my-client-id'
    assert authenticator.secret == 'my-client-secret'
    assert authenticator.refresh_token == 'my-refresh-token'


def test_audio_lifecycle_extend_audio_ping(
    lifecycle, mock_client_send_conditional_ping
):
    lifecycle.extend_audio(b'\x05\x00\x05\x00')

    assert mock_client_send_conditional_ping.call_count == 1


def test_audio_lifecycle_handle_command_started_websocket_message(lifecycle):
    with patch.object(lifecycle, 'send_command_to_avs'):
        lifecycle.handle_command_started()

    assert lifecycle.reply_channel.send.call_count == 1
    assert lifecycle.reply_channel.send.call_args == call(
        {'text': '{"type": "EXPECTING_COMMAND"}'},
        immediately=True
    )


def test_audio_lifecycle_handle_command_started_sends_avs_command(lifecycle):
    with patch.object(lifecycle, 'send_command_to_avs') as stub_send_command:
        lifecycle.handle_command_started()

    assert stub_send_command.call_count == 1


def test_audio_lifecycle_handle_command_finished_websocket_message(lifecycle):
    lifecycle.handle_command_finised()

    assert lifecycle.reply_channel.send.call_count == 1
    assert lifecycle.reply_channel.send.call_args == call(
        {'text': '{"type": "EXPECTING_WAKEWORD"}'}, immediately=True
    )


def test_audio_lifecycle_sends_command_to_avs_sends_audio_file(lifecycle):
    with patch('command_lifecycle.helpers.LifeCycleFileLike') as mock_filelike:
        lifecycle.send_command_to_avs()

    assert mock_filelike.call_args == call(lifecycle)
    assert lifecycle.alexa_client.send_audio_file.call_count == 1
    assert lifecycle.alexa_client.send_audio_file.call_args == call(
        audio_file=mock_filelike(),
        context=None,
    )


def test_audio_lifecycle_sends_command_to_avs_websocket_message(
    lifecycle, mock_client_send_audio_file
):
    mock_client_send_audio_file.return_value = b'thing'

    lifecycle.send_command_to_avs()

    assert lifecycle.reply_channel.send.call_count == 1
    assert lifecycle.reply_channel.send.call_args == call({'bytes': b'thing'})
