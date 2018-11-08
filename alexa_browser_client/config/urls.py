from django.urls import path, include

from alexa_browser_client.alexa_browser_client import (
    views as alexa_browser_client_views
)
from alexa_browser_client.refreshtoken import views as refreshtoken_views


oauth2_urlpatterns = [
    path(
        '',
        refreshtoken_views.AmazonAuthorizationRequestRedirectView.as_view(),
        name='refreshtoken',
    ),
    path(
        'callback/',
        refreshtoken_views.AmazonOauth2AuthorizationGrantView.as_view(),
        name='refreshtoken-callback',
    ),
]

urlpatterns = [
    path(
        '',
        alexa_browser_client_views.AlexaBrowserClientView.as_view(),
        name='alexa-browser-client',
    ),
    path('refreshtoken/', include(oauth2_urlpatterns)),
]
