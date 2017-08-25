from django.conf.urls import url

from alexa_browser_client.alexa_browser_client import views


urlpatterns = [
    url(
        r'^alexa-browser-client/$',
        views.AlexaBrowserClientView.as_view(),
        name='alexa-browser-client',
    ),
]
