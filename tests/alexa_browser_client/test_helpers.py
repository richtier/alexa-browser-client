import pytest
from unittest.mock import call, patch, Mock

from alexa_browser_client.alexa_browser_client import helpers


@pytest.fixture
def reply_channel():
    return Mock()


@pytest.fixture
def lifecycle(reply_channel):
    class TestAudioLifecycle(helpers.AudioLifecycle):
        alexa_client_class = Mock()
        audio_detector_class = Mock()
    return TestAudioLifecycle(reply_channel=reply_channel)


def test_audio_lifecycle_connects_to_avs(lifecycle):
    assert lifecycle.alexa_client.connect.call_count == 1


def test_audio_lifecycle_sets_attributes(reply_channel):
    lifecycle = helpers.AudioLifecycle(reply_channel=reply_channel)
    authenticator = lifecycle.alexa_client.authentication_manager

    assert lifecycle.reply_channel == reply_channel
    assert authenticator.client_id == 'my-client-id'
    assert authenticator.secret == 'my-client-secret'
    assert authenticator.refresh_token == 'my-refresh-token'


def test_audio_lifecycle_extend_audio_ping(lifecycle):
    lifecycle.extend_audio(b'\x05\x00')

    assert lifecycle.alexa_client.conditional_ping.call_count == 1


def test_audio_lifecycle_handle_command_started_websocket_message(lifecycle):
    with patch.object(lifecycle, 'send_command_to_avs'):
        lifecycle.handle_command_started()

    assert lifecycle.reply_channel.send.call_count == 1
    assert lifecycle.reply_channel.send.call_args == call(
        {'text': '{"type": "EXPECTING_COMMAND", "payload": true}'},
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
        {'text': '{"type": "EXPECTING_COMMAND", "payload": false}'},
    )


def test_audio_lifecycle_sends_command_to_avs_sends_audio_file(lifecycle):
    with patch('command_lifecycle.helpers.LifeCycleFileLike') as mock_filelike:
        lifecycle.send_command_to_avs()

    assert mock_filelike.call_args == call(lifecycle)
    assert lifecycle.alexa_client.send_audio_file.call_count == 1
    assert lifecycle.alexa_client.send_audio_file.call_args == call(
        mock_filelike()
    )


def test_audio_lifecycle_sends_command_to_avs_websocket_message(lifecycle):
    lifecycle.alexa_client.send_audio_file.return_value = b'thing'

    lifecycle.send_command_to_avs()

    assert lifecycle.reply_channel.send.call_count == 1
    assert lifecycle.reply_channel.send.call_args == call({'bytes': b'thing'})


def test_audio_lifecycle_alexa_voice_service_client(settings, lifecycle):
    assert lifecycle.alexa_client_class.call_count == 1
    assert lifecycle.alexa_client_class.call_args == call(
        client_id='my-client-id',
        secret='my-client-secret',
        refresh_token='my-refresh-token',
    )
