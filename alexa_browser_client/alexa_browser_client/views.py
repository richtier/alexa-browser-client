from django.core.urlresolvers import reverse
from django.views.generic import TemplateView


class AlexaBrowserClientView(TemplateView):
    template_name = 'alexa_browser_client/alexa-browser-client.html'
