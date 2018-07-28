Alexa Browser Client
====================

|code-climate-image| |circle-ci-image| [[codecov-image]][codecov]

**Alexa client in your browser. Django app. Talk to Alexa from your
desktop, phone, or tablet browser.**

--------------

Demo
----

The demo should really be heard, so click the gif below to view it in
youtube.

|Demo|

Dependencies
------------

This project depends on: -
`django-channels <https://channels.readthedocs.io/en/stable/>`__. -
`Snowboy <https://github.com/Kitt-AI/snowboy#compile-a-python-wrapper>`__

Install and configure those first.

Snowboy
~~~~~~~

`Snowboy <https://github.com/Kitt-AI/snowboy#compile-a-python-wrapper>`__
detects when the wakeword "Alexa" is uttered.

You must compile
`Snowboy <https://github.com/Kitt-AI/snowboy#compile-a-python-wrapper>`__
manually. Copy the compiled ``snowboy`` folder to the top level of you
project. By default, the folder structure should be:

::

    .
    ├── ...
    ├── snowboy
    |   ├── snowboy-detect-swig.cc
    |   ├── snowboydetect.py
    |   └── resources
    |       ├── alexa.umdl
    |       └── common.res
    └── ...

If the default folder structure does not suit your needs you can
`customize the wakeword detector <#wakeword>`__.

Installation
------------

::

    pip install alexa_browser_client

Make sure your settings ``INSTALLED_APPS`` contains at least these
entries:

::

    INSTALLED_APPS = [
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'channels',
        'alexa_browser_client',
    ]

Routing and urls
~~~~~~~~~~~~~~~~

Add ``url(r'^', include('alexa_browser_client.config.urls')),`` to
``urls.py`` ``url_patterns``.

Add ``include('alexa_browser_client.config.routing.channel_routing')``
to your ``routing.py`` ``channel_routing``.

Authentication
--------------

This app uses Alexa Voice Service. To use AVS you must first have a
`developer account <http://developer.amazon.com>`__. Then register your
product
`here <https://developer.amazon.com/avs/home.html#/avs/products/new>`__.
Choose "Application" under "Is your product an app or a device"?

Ensure you update your settings.py:

+-------------------------------------+--------------------------------------+
| Setting                             | Notes                                |
+=====================================+======================================+
| ``ALEXA_BROWSER_CLIENT_AVS_CLIENT_I | Retrieve by clicking on the your     |
| D``                                 | product listed                       |
|                                     | `here <https://developer.amazon.com/ |
|                                     | avs/home.html#/avs/home>`__          |
+-------------------------------------+--------------------------------------+
| ``ALEXA_BROWSER_CLIENT_AVS_CLIENT_S | Retrieve by clicking on the your     |
| ECRET``                             | product listed                       |
|                                     | `here <https://developer.amazon.com/ |
|                                     | avs/home.html#/avs/home>`__          |
+-------------------------------------+--------------------------------------+
| ``ALEXA_BROWSER_CLIENT_AVS_DEVICE_T | Retrieve by reading "Product ID"     |
| YPE_ID``                            | `here <https://developer.amazon.com/ |
|                                     | avs/home.html#/avs/home>`__          |
+-------------------------------------+--------------------------------------+

Refresh token
~~~~~~~~~~~~~

You will need to login to Amazon via a web browser to get your refresh
token.

To enable this first go
`here <https://developer.amazon.com/avs/home.html#/avs/home>`__ and
click on your product to set some security settings under
``Security Profile`` and, assuming you're running on localhost:8000, set
the following:

+-----------------------+-------------------------------------------------+
| setting               | value                                           |
+=======================+=================================================+
| Allowed Origins       | https://localhost:8000/refreshtoken/            |
+-----------------------+-------------------------------------------------+
| Allowed Return URLs   | https://localhost:8000/refreshtoken/callback/   |
+-----------------------+-------------------------------------------------+

Usage
-----

Once you have all the settings configured:

-  Run django: ``./manage.py runserver``
-  Go to ``http://localhost:8000`` and start talking to Alexa.

Customization
-------------

Wakeword
~~~~~~~~

The default wakeword is "Alexa". You can change this by customizing the
lifecycle's ``audio_detector_class``:

.. code:: py

    # my_project/consumers.py

    import alexa_browser_client
    import command_lifecycle


    class CustomAudioDetector(command_lifecycle.wakeword.SnowboyWakewordDetector):
        wakeword_library_import_path = 'dotted.import.path.to.wakeword.Detector'
        resource_file = b'path/to/resource_file.res'
        decoder_model = b'path/to/model_file.umdl'


    class CustomAudioLifecycle(alexa_browser_client.AudioLifecycle):
        audio_detector_class = CustomAudioDetector


    class CustomAlexaConsumer(alexa_browser_client.AlexaConsumer):
        audio_lifecycle_class = CustomAudioLifecycle

Then in your ``routes.py``:

::

    from my_project import consumers


    channel_routing = [
        consumers.CustomAlexaConsumer.as_route(path='/'),
    ]

Unit test
---------

To run the unit tests, call the following commands:

.. code:: sh

    pip install -r requirements-dev.txt
    ./scripts/tests.sh

To test a specific file, call the following command:

.. code:: sh

    ./scripts/tests.sh /path/to/test-file.py

Versioning
----------

We use `SemVer <http://semver.org/>`__ for versioning. For the versions
available, see the
`PyPI <https://pypi.org/project/alexa-browser-client/#history>`__.

Other projects
--------------

This project uses `Voice Command
Lifecycle <https://github.com/richtier/voice-command-lifecycle>`__ and
`Alexa Voice Service
Client <https://github.com/richtier/alexa-voice-service-client>`__.

.. |code-climate-image| image:: https://codeclimate.com/github/richtier/alexa-browser-client/badges/gpa.svg
   :target: https://codeclimate.com/github/richtier/alexa-browser-client
.. |circle-ci-image| image:: https://circleci.com/gh/richtier/alexa-browser-client/tree/master.svg?style=svg
   :target: https://circleci.com/gh/richtier/alexa-browser-client/tree/master
.. |Demo| image:: https://j.gifs.com/qY4qBy.gif
   :target: https://youtu.be/cm19aa6x9VY
