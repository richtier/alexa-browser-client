from django.conf.urls import url, include

from alexa_browser_client.alexa_browser_client import (
    views as alexa_browser_client_views
)
from alexa_browser_client.refreshtoken import (
    views as refreshtoken_views
)


oauth2_urlpatterns = [
    url(
        r'^$',
        refreshtoken_views.AmazonAuthorizationRequestRedirectView.as_view(),
        name='refreshtoken',
    ),
    url(
        r'^callback/$',
        refreshtoken_views.AmazonOauth2AuthorizationGrantView.as_view(),
        name='refreshtoken-callback',
    ),
]

urlpatterns = [
    url(
        r'^$',
        alexa_browser_client_views.AlexaBrowserClientView.as_view(),
        name='alexa-browser-client',
    ),
    url(r'^refreshtoken/', include(oauth2_urlpatterns)),
]
