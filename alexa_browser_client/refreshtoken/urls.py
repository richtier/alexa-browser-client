from django.conf.urls import url

from alexa_browser_client.refreshtoken import views


urlpatterns = [
    url(
        r'^amazon-login/$',
        views.AmazonAlexaServiceLoginView.as_view(),
        name='amazon-login'
    ),
    url(
        r'^amazon-login/authresponse/$',
        views.AmazonAlexaServiceLoginCallback.as_view(),
        name='amazon-authresponse'
    ),
]
