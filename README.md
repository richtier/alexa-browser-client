# alexa-browser-client
Alexa client in your browser. Django app.

Talk to Alexa from your desktop, phone, or tablet browser.

## Installation

This project also depends on [django-channels](https://channels.readthedocs.io/en/stable/). Install and set that up that first.

```
pip install git+https://github.com/richtier/alexa-browser-client.git@v0.2.0#egg=alexa_browser_client
```

Add `alexa_browser_client` to your settings `INSTALLED_APPS`.

### Wakeword detector ###
A wakeword is a specific word that triggers the code to spring into action (such as "Alexa"). This app uses [snowboy](https://github.com/Kitt-AI/snowboy#compile-a-python-wrapper) to determine if the wakeword was uttered. Snowboy will need to be installed first.

Once you have compiled snowboy, copy the compiled `snowboy` folder to the top level of you project. By default, the folder structure should be:
```
.
├── ...
├── snowboy
|   ├── snowboy-detect-swig.cc
|   ├── snowboydetect.py
|   └── resources
|       ├── alexa.umdl
|       └── common.res
└── ...
```

If the default structure does not suit your needs can [customize the wakeword detector](#wakeword).

### Routing and urls
Add `url(r'^', include('alexa_browser_client.config.urls')),` to `urls.py` `url_patterns`.

Add `include('alexa_browser_client.config.routing.channel_routing')` to your `routing.py` `channel_routing`.

## Authentication ##

You must first have a [developer account](http://developer.amazon.com). Then register your product [here](https://developer.amazon.com/avs/home.html#/avs/products/new). Choose "Application" under "Is your product an app or a device"?

Ensure you update your settings.py:

| Setting                             | Notes                                 |
| ----------------------------------- | ------------------------------------- |
| `ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID`     | Retrieve by clicking on the your product listed [here](https://developer.amazon.com/avs/home.html#/avs/home)   |
| `ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET` | Retrieve by clicking on the your product listed [here](https://developer.amazon.com/avs/home.html#/avs/home)   |
| `ALEXA_BROWSER_CLIENT_AVS_REFRESH_TOKEN` | You must generate this. [See here](#refresh-token)                                                               |

### Refresh token ###

You will need to login to Amazon via a web browser to get your refresh token.

To enable this first go [here](https://developer.amazon.com/avs/home.html#/avs/home) and click on your product to set some security settings under `Security Profile`:

| setting             | value                            |
| ------------------- | ---------------------------------|
| Allowed Origins     | https://localhost:9000           |
| Allowed Return URLs | https://localhost:9000/callback/ |

Then run:

```sh
./manage.py create_amazon_refresh_token
```

Follow the on-screen instructions shown at `http://localhost:9000` in your web browser. On completion Amazon will return your `refresh_token`. Set your`ALEXA_VOICE_SERVICE_REFRESH_TOKEN` setting accordingly.

## Usage

Once you have all the settings configured:

- Run django: `./manage.py runserver localhost:8080`
- Go to `http://localhost:8080/alexa-browser-client/` and start talking to Alexa.

## Customization ##

### Wakeword ###

The default wakeword is "Alexa". You can change this by customizing the lifecycle's `audio_detector_class`:

```py
# my_project/custom.py

import alexa_browser_client
import command_lifecycle


class CustomAudioDetector(command_lifecycle.wakeword.SnowboyWakewordDetector):
    wakeword_library_import_path = 'dotted.import.path.to.wakeword.Detector'
    resource_file = b'path/to/resource_file.res'
    decoder_model = b'path/to/model_file.umdl'


class CustomAudioLifecycle(alexa_browser_client.AudioLifecycle):
    audio_detector_class = CustomAudioDetector
```

Then in your `settings.py`, change
`settings.AUDIO_LIFECYCLE_CLASS` to the new custom audio lifecycle:

```py
ALEXA_BROWSER_CLIENT_LIFECYCLE_CLASS = 'my_project.custom.CustomAudioLifecycle'
```

## Other projects

This project uses [Voice Command Lifecycle](https://github.com/richtier/voice-command-lifecycle) and [Alexa Voice Service Client](https://github.com/richtier/alexa-voice-service-client).
