from unittest import mock

from avs_client import AlexaVoiceServiceClient
from channels.testing import WebsocketCommunicator
from requests.exceptions import HTTPError
import pytest

from alexa_browser_client import consumers, constants


MESSAGE_CONNECTING = {'type': constants.CONNECTING}
MESSAGE_CLOSED = {'code': 3000, 'type': 'websocket.close'}
MESSAGE_WAKEWORD = {'type': constants.EXPECTING_WAKEWORD}
MESSAGE_COMMAND = {'type': constants.EXPECTING_COMMAND}


@pytest.fixture(autouse=True)
def mock_client_connect():
    stub = mock.patch.object(AlexaVoiceServiceClient, 'connect')
    yield stub.start()
    stub.stop()


@pytest.mark.asyncio
async def test_connect_rejected_no_refresh_token():
    communicator = WebsocketCommunicator(consumers.AlexaConsumer, '/')
    communicator.scope['session'] = {}
    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_output() == MESSAGE_CLOSED

    await communicator.disconnect()


@pytest.mark.asyncio
async def test_connect_rejected_invalid_refresh_token(
    mock_client_connect
):
    mock_client_connect.side_effect = HTTPError()

    communicator = WebsocketCommunicator(consumers.AlexaConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}
    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_output() == MESSAGE_CLOSED

    await communicator.disconnect()


@pytest.mark.asyncio
async def test_connected_expecting_wakeword():
    communicator = WebsocketCommunicator(consumers.AlexaConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}

    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD

    await communicator.disconnect()


@pytest.mark.asyncio
async def test_connected_create_audio_lifecycle():
    communicator = WebsocketCommunicator(consumers.AlexaConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}

    connected, subprotocol = await communicator.connect()

    assert connected

    await communicator.disconnect()

    assert (
        communicator.instance.audio_lifecycle.on_command_started ==
        communicator.instance.handle_command_started
    )
    assert (
        communicator.instance.audio_lifecycle.on_command_finished ==
        communicator.instance.handle_command_finished
    )


@pytest.mark.asyncio
async def test_receive():
    communicator = WebsocketCommunicator(consumers.AlexaConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}

    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD
    assert await communicator.receive_nothing()

    instance = communicator.instance
    instance.audio_lifecycle.extend_audio = mock.Mock()
    instance.alexa_client.conditional_ping = mock.Mock()

    await communicator.send_to(bytes_data=b'01')
    await communicator.disconnect()

    assert instance.audio_lifecycle.extend_audio.call_count == 1
    assert instance.audio_lifecycle.extend_audio.call_args == mock.call(b'01')

    assert instance.alexa_client.conditional_ping.call_count == 1
