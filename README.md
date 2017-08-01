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

```
| setting | Notes                                                                |
|---------------|----------------------------------------------------------------------|
| ALEXA_VOICE_SERVICE_CLIENT_ID     | See AVS documentation [link 1, below)                                |
| ALEXA_VOICE_SERVICE_CLIENT_SECRET        | See AVS documentation [link 1, below)                                |
| ALEXA_VOICE_SERVICE_REFRESH_TOKEN | Set this to the value returned when you retrieve your refresh token. |
```

[1] https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/docs/authorizing-your-alexa-enabled-product-from-a-website#lwa

### refresh token
TODO: expose alexa-voice-service-client's refresh token retrieval code

## Usage
- Run django: `./manage.py runserver localhost:8000`
- Go to `http://localhost:8000/alexa-browser-client/` and start talking to Alexa.

## Other projects

This project uses [Voice Command Lifecycle](https://github.com/richtier/voice-command-lifecycle) and [Alexa Voice Service Client](https://github.com/richtier/alexa-voice-service-client).
