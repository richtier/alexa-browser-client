# alexa-browser-client
Alexa client in your browser. Django app.

Talk to Alexa from your desktop, phone, or tablet browser.

## Installation

This project also depends on [django-channels](https://channels.readthedocs.io/en/stable/). Install and set that up that first.

```
pip install git+https://github.com/richtier/alexa-browser-client.git@v0.1.0#egg=alexa_browser_client
```

Add `alexa_browser_client` to your settings `INSTALLED_APPS`.

### Routing and urls
Add `url(r'^', include('alexa_browser_client.alexa_browser_client.urls')),` to `urls.py` `url_patterns`.

Add `include('alexa_browser_client.alexa_browser_client.routing.channel_routing')` to your `routing.py` `channel_routing`.

### settings.py

Valid authentication details are required to communicate with AVS. Set the following in your `settings.py`:

| setting | Notes                                                                |
| --------------- | ---------------------------------------------------------------------- |
| ALEXA_VOICE_SERVICE_CLIENT_ID     | See [AVS documentation](https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/docs/authorizing-your-alexa-enabled-product-from-a-website#lwa)                                |
| ALEXA_VOICE_SERVICE_CLIENT_SECRET        | See [AVS documentation](https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/docs/authorizing-your-alexa-enabled-product-from-a-website#lwa)                                |
| ALEXA_VOICE_SERVICE_REFRESH_TOKEN | See [below](#refresh-token) |

### Refresh token
When the client authenticates with AVS using the authentication values specified in  `ALEXA_VOICE_SERVICE_CLIENT_ID` and `ALEXA_VOICE_SERVICE_CLIENT_SECRET` AVS returns an access token that authorizes subsequent requests. The access token expires after an hour. To have AVS automatically generate a new access token once the old one expires, set your `ALEXA_VOICE_SERVICE_REFRESH_TOKEN` setting.

To get your refresh token for the first time you will need to authenticate with Amazon via their web interface. To do this run:

```sh
./manage.py create_amazon_refresh_token
```

Then go to `http://localhost:8000` and follow the on-screen instructions. Use the `refresh_token` returned by Amazon in your `ALEXA_VOICE_SERVICE_REFRESH_TOKEN` setting.

## Usage

Once you have all the settings configured:

- Run django: `./manage.py runserver localhost:8080`
- Go to `http://localhost:8080/alexa-browser-client/` and start talking to Alexa.

## Other projects

This project uses [Voice Command Lifecycle](https://github.com/richtier/voice-command-lifecycle) and [Alexa Voice Service Client](https://github.com/richtier/alexa-voice-service-client).
