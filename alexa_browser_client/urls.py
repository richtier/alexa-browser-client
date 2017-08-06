from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('alexa_browser_client.alexa_browser_client.urls')),
]
