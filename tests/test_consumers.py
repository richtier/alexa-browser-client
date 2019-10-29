from unittest import mock

from alexa_client.alexa_client.helpers import Directive, SpeakDirective
from channels.testing import WebsocketCommunicator
from requests.exceptions import HTTPError
import pytest

from alexa_browser_client import consumers, constants, helpers


MESSAGE_CONNECTING = {'type': constants.CONNECTING}
MESSAGE_CLOSED = {'code': 3000, 'type': 'websocket.close'}
MESSAGE_WAKEWORD = {'type': constants.EXPECTING_WAKEWORD}
MESSAGE_COMMAND = {'type': constants.EXPECTING_COMMAND}


class AlexaClientCommandNotUnderstood(mock.Mock):
    # consumer receives audio that AVS does not understand
    send_audio_file = mock.Mock(return_value=[])


class AlexaClientPlayResponse(mock.Mock):
    send_audio_file = mock.Mock(return_value=[
        SpeakDirective(
            audio_attachment=b'22222222',
            content={
                'directive': {},
                'header': {'name': 'Play', 'dialogRequestId': '123'}
            }
        )
    ])


class AlexaClientExpectSpeechResponse(mock.Mock):
    send_audio_file = mock.Mock(return_value=[
        Directive({
            'directive': {},
            'header': {'name': 'ExpectSpeech', 'dialogRequestId': '123'}
        })
    ])


class AlexaClientSpeakResponse(mock.Mock):
    send_audio_file = mock.Mock(return_value=[
        SpeakDirective(
            audio_attachment=b'22222222',
            content={
                'directive': {},
                'header': {'name': 'Speak', 'dialogRequestId': '123'}
            }
        )
    ])


class ImmediateCommandLifecycle(helpers.AudioLifecycle):

    def get_uttered_wakeword_name(self):
        yield 'TEST'
        yield None


@pytest.fixture(autouse=True)
def alexa_client():
    patch = mock.patch('alexa_client.AlexaClient')
    yield patch.start()
    patch.stop()


@pytest.fixture
def audio_lifecycle():
    patch = mock.patch(
        'alexa_browser_client.consumers.AlexaConsumer.audio_lifecycle_class'
    )
    yield patch.start()
    patch.stop()


# @pytest.fixture
# def send():
#     patch = mock.patch.object(
#         consumers.AlexaConsumer, 'send',
#         # wraps=consumers.AlexaConsumer.send
#     )
#     yield patch.start()
#     patch.stop()


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
async def test_connect_rejected_invalid_refresh_token(alexa_client):

    alexa_client.connect.side_effect = HTTPError()

    communicator = WebsocketCommunicator(consumers.AlexaConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}
    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_output() == MESSAGE_CLOSED

    await communicator.disconnect()


@pytest.mark.asyncio
async def test_connected_expecting_wakeword():

    class TestConsumer(consumers.AlexaConsumer):
        audio_lifecycle_class = ImmediateCommandLifecycle
        alexa_client_class = mock.Mock

    communicator = WebsocketCommunicator(TestConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}

    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD
    assert await communicator.receive_nothing()
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_receive_audio():

    class TestCommandLifecycle(helpers.AudioLifecycle):
        get_uttered_wakeword_name = mock.Mock(return_value=None)
        extend_audio = mock.Mock()

    class TestConsumer(consumers.AlexaConsumer):
        audio_lifecycle_class = TestCommandLifecycle
        alexa_client_class = AlexaClientExpectSpeechResponse

    communicator = WebsocketCommunicator(TestConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}

    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD
    assert await communicator.receive_nothing()

    await communicator.send_to(bytes_data=b'01010101')
    await communicator.disconnect()

    assert TestCommandLifecycle.extend_audio.call_count == 1
    assert TestCommandLifecycle.extend_audio.call_args == (
        mock.call(b'01010101')
    )


@pytest.mark.asyncio
async def test_receive_speak_prompt(audio_lifecycle):

    class TestConsumer(consumers.AlexaConsumer):
        audio_lifecycle_class = ImmediateCommandLifecycle
        alexa_client_class = AlexaClientExpectSpeechResponse

    communicator = WebsocketCommunicator(TestConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}

    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD
    assert await communicator.receive_nothing()

    audio_lifecycle.extend_audio = mock.Mock()
    audio_lifecycle.handle_command_started = mock.Mock()

    await communicator.send_to(text_data='ExpectSpeech')

    assert await communicator.receive_json_from() == MESSAGE_COMMAND

    await communicator.disconnect()


@pytest.mark.asyncio
async def test_send_command_to_avs_expect_speech(alexa_client):
    class TestConsumer(consumers.AlexaConsumer):
        audio_lifecycle_class = ImmediateCommandLifecycle
        alexa_client_class = AlexaClientExpectSpeechResponse

        def handle_command_started(self, wakeword_name):
            super().handle_command_started(wakeword_name)
            self.send_command_to_avs()

    communicator = WebsocketCommunicator(TestConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}

    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD
    assert await communicator.receive_nothing()

    await communicator.send_to(text_data='ExpectSpeech')
    assert await communicator.receive_json_from() == MESSAGE_COMMAND
    await communicator.send_to(bytes_data=b'01010101')

    await communicator.disconnect()

    assert await communicator.receive_json_from() == {'type': 'ExpectSpeech'}
    assert await communicator.receive_json_from() == {'type': 'ExpectSpeech'}
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD

    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'client_class', [AlexaClientPlayResponse, AlexaClientSpeakResponse]
)
async def test_send_command_to_avs_speak(client_class, alexa_client):

    class TestConsumer(consumers.AlexaConsumer):
        audio_lifecycle_class = ImmediateCommandLifecycle
        alexa_client_class = client_class

        def handle_command_started(self, wakeword_name):
            super().handle_command_started(wakeword_name)
            self.send_command_to_avs()

    communicator = WebsocketCommunicator(TestConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}

    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD
    assert await communicator.receive_nothing()

    assert await communicator.receive_nothing()
    await communicator.send_to(text_data='ExpectSpeech')
    assert await communicator.receive_json_from() == MESSAGE_COMMAND
    await communicator.send_to(bytes_data=b'01010101')

    assert await communicator.receive_from() == b'22222222'
    await communicator.disconnect()


@pytest.mark.asyncio
async def test_send_command_to_avs_not_understood():

    class TestConsumer(consumers.AlexaConsumer):
        audio_lifecycle_class = ImmediateCommandLifecycle
        alexa_client_class = AlexaClientCommandNotUnderstood

        def handle_command_started(self, wakeword_name):
            super().handle_command_started(wakeword_name)
            self.send_command_to_avs()

    communicator = WebsocketCommunicator(TestConsumer, '/')
    communicator.scope['session'] = {constants.SESSION_KEY_REFRESH_TOKEN: '1'}

    connected, subprotocol = await communicator.connect()

    assert connected
    assert await communicator.receive_json_from() == MESSAGE_CONNECTING
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD
    assert await communicator.receive_nothing()
    await communicator.send_to(text_data='ExpectSpeech')
    assert await communicator.receive_json_from() == MESSAGE_COMMAND
    await communicator.send_to(bytes_data=b'01010101')
    assert await communicator.receive_json_from() == MESSAGE_WAKEWORD

    await communicator.disconnect()
