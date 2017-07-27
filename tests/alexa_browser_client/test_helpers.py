import pytest
from unittest.mock import call, patch, Mock

from alexa_browser_client.alexa_browser_client import helpers


@pytest.fixture
def reply_channel():
    return Mock()


@pytest.fixture
def lifecycle(reply_channel):
    stub = patch.object(helpers.AudioLifecycle, 'alexa_client')
    stub.start()
    yield helpers.AudioLifecycle(reply_channel=reply_channel)
    stub.stop()


def test_audio_lifecycle_connects_to_avs(lifecycle):
    assert lifecycle.alexa_client.connect.call_count == 1


def test_audio_lifecycle_sets_attributes(reply_channel):
    lifecycle = helpers.AudioLifecycle(reply_channel=reply_channel)
    authenticator = lifecycle.alexa_client.authenticator

    assert lifecycle.reply_channel == reply_channel
    assert authenticator.client_id == 'my-client-id'
    assert authenticator.secret == 'my-client-secret'
    assert authenticator.refresh_token == 'my-refresh-token'


@pytest.mark.parametrize('should_ping,call_count', [[True, 1], [False, 0]])
def test_audio_lifecycle_extend_audio_ping(should_ping, call_count, lifecycle):
    lifecycle.alexa_client.should_ping.return_value = should_ping

    lifecycle.extend_audio(b'\x05\x00')

    assert lifecycle.alexa_client.ping.call_count == call_count


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
    with patch.object(helpers, 'LifeCycleFileLike') as mock_filelike:
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


def test_lifecycle_filelike_reads_from_buffer(lifecycle):
    lifecycle.extend_audio(b'12345678')

    file_like = helpers.LifeCycleFileLike(lifecycle)

    assert file_like.read(4) == b'1234'
    assert file_like.read(4) == b'5678'


def test_lifecycle_filelike_length_not_expecting_audio(lifecycle):
    lifecycle.extend_audio(b'12345678')
    lifecycle.is_command_pending = False

    file_like = helpers.LifeCycleFileLike(lifecycle)

    assert len(file_like) == 8


def test_lifecycle_filelike_length_expecting_audio(lifecycle):
    lifecycle.extend_audio(b'12345678')
    lifecycle.is_command_pending = True

    file_like = helpers.LifeCycleFileLike(lifecycle)

    assert len(file_like) == 1025
