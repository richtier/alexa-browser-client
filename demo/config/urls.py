from django.urls import path

from alexa_browser_client.config.urls import urlpatterns

from demo import views

urlpatterns += [
    path('mixer/', views.AlexaBrowserClientMixerView.as_view()),
]
