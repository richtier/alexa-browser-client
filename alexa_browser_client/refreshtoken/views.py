from collections import OrderedDict
import json
import requests
from urllib.parse import urlencode, quote

from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.generic import RedirectView, View


class AmazonAlexaServiceLoginView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # note: ensure the redirect url is whitelisted in the
        # "Allowed Return URLs" section under 'Web Settings' for your
        # Security Profile on Amazon Developer Portal.
        url = reverse('amazon-authresponse')
        # OrderedDict to facilitate testing
        params = OrderedDict([
            ('client_id', settings.CLIENT_ID),
            ('scope', 'alexa:all'),
            ('scope_data', json.dumps({
                'alexa:all': OrderedDict([
                    ('productID', settings.DEVICE_TYPE_ID),
                    ('productInstanceAttributes', {
                        'deviceSerialNumber': '001'
                    })
                ])
            })),
            ('response_type', 'code'),
            ('redirect_uri', self.request.build_absolute_uri(url))
        ])
        return 'https://www.amazon.com/ap/oa?' + urlencode(params)


class AmazonAlexaServiceLoginCallback(View):
    oauth2_url = 'https://api.amazon.com/auth/o2/token'

    def get(self, request, *args, **kwargs):
        url = reverse('amazon-authresponse')
        payload = {
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'code': quote(request.GET['code']),
            'grant_type': 'authorization_code',
            'redirect_uri': self.request.build_absolute_uri(url),
        }
        response = requests.post(self.oauth2_url, json=payload)
        if response.status_code != 200:
            return HttpResponse(response.content, status=response.status_code)
        return JsonResponse(response.json())
