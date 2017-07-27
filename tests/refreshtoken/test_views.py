import urllib

import pytest

from alexa_browser_client.refreshtoken import views


@pytest.fixture
def oauth2_retrieve_200(requests_mocker):
    return requests_mocker.post(
        views.AmazonAlexaServiceLoginCallback.oauth2_url,
        json={'refresh_token': '12345'}
    )


def test_login_view_redirect_url(rf):
    view = views.AmazonAlexaServiceLoginView.as_view()
    request = rf.get('/')

    response = view(request)

    assert urllib.parse.unquote_plus(response.get('Location')) == (
        'https://www.amazon.com/ap/oa?client_id=my-client-id&scope=alexa:all'
        '&scope_data={"alexa:all": {"productID": "my-device-type-id", '
        '"productInstanceAttributes": {"deviceSerialNumber": "001"}}}&'
        'response_type=code&'
        'redirect_uri=http://testserver/amazon-login/authresponse/'
    )


def test_login_view_callback_calls_amazon(rf, oauth2_retrieve_200):

    view = views.AmazonAlexaServiceLoginCallback.as_view()
    request = rf.get('/', {'code': 123})

    view(request)

    assert oauth2_retrieve_200.last_request.url == (
        views.AmazonAlexaServiceLoginCallback.oauth2_url
    )
    assert oauth2_retrieve_200.last_request.json() == {
        'client_secret': 'my-client-secret',
        'client_id': 'my-client-id',
        'redirect_uri': 'http://testserver/amazon-login/authresponse/',
        'grant_type': 'authorization_code',
        'code': '123'
    }


def test_login_view_callback_returns_amazon_response(rf, oauth2_retrieve_200):

    view = views.AmazonAlexaServiceLoginCallback.as_view()
    request = rf.get('/', {'code': 123})

    response = view(request)

    assert response.status_code == 200
    assert response.content == b'{"refresh_token": "12345"}'


@pytest.mark.parametrize("status_code",  [code for code in range(201, 600)])
def test_login_view_callback_handles_bad_amazon_response(
    status_code, rf, requests_mocker
):
    requests_mocker.post(
        views.AmazonAlexaServiceLoginCallback.oauth2_url,
        status_code=status_code,
        text='Something went wrong.',
    )

    view = views.AmazonAlexaServiceLoginCallback.as_view()
    request = rf.get('/', {'code': 123})

    response = view(request)

    assert response.status_code == status_code
    assert response.content == b'Something went wrong.'
