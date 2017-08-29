from django.core.urlresolvers import reverse

from alexa_browser_client.alexa_browser_client import views


def test_alexa_browser_client_view(client):
    response = client.get(reverse('alexa-browser-client'))

    assert response.status_code == 200
    assert response.template_name == [
        views.AlexaBrowserClientView.template_name
    ]
    assert response.context_data['websocket_url'] == (
        'ws://testserver/alexa-browser-client/'
    )
