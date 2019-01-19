from django.urls import path, include

from alexa_browser_client import views


oauth2_urlpatterns = [
    path(
        '',
        views.AmazonAuthorizationRequestRedirectView.as_view(),
        name='refreshtoken',
    ),
    path(
        'callback/',
        views.AmazonOauth2AuthorizationGrantView.as_view(),
        name='refreshtoken-callback',
    ),
]

urlpatterns = [
    path('', views.AlexaBrowserClientView.as_view()),
    path('refreshtoken/', include(oauth2_urlpatterns)),
]
