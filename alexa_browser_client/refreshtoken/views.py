from avs_client.refreshtoken.helpers import AmazonOauth2RequestManager
import requests

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from . import constants, forms


class Oauth2Mixin:
    @property
    def oauth2_manager(self):
        return AmazonOauth2RequestManager(
            client_id=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_ID,
            client_secret=settings.ALEXA_BROWSER_CLIENT_AVS_CLIENT_SECRET,
        )

    @property
    def callback_url(self):
        url = reverse('refreshtoken-callback')
        return self.request.build_absolute_uri(url)

    @property
    def redirect_url(self):
        url = self.request.session.get(constants.SESSION_KEY_REDIRECT_URL)
        return url or '/'

    @redirect_url.setter
    def redirect_url(self, value):
        self.request.session[constants.SESSION_KEY_REDIRECT_URL] = value


class SubmitFormOnGetMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['data'] = self.request.GET or {}
        return kwargs

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AmazonAuthorizationRequestRedirectView(Oauth2Mixin, RedirectView):

    def dispatch(self, *args, **kwargs):
        self.redirect_url = self.request.GET.get('redirect_url')
        return super().dispatch(*args, **kwargs)

    def get_redirect_url(self):
        return self.oauth2_manager.get_authorization_request_url(
            device_type_id=settings.ALEXA_BROWSER_CLIENT_AVS_DEVICE_TYPE_ID,
            callback_url=self.callback_url,
        )


class AmazonOauth2AuthorizationGrantView(
    Oauth2Mixin, SubmitFormOnGetMixin, FormView
):
    form_class = forms.CompaniesHouseOauth2Form

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        payload = self.oauth2_manager.get_authorizarization_grant_params(
            code=form.cleaned_data['code'],
            callback_url=self.callback_url,
        )
        response = requests.post(
            self.oauth2_manager.authorization_grant_url, json=payload
        )
        if response.status_code != 200:
            return JsonResponse(response.json(), status=response.status_code)
        self.request.session[constants.SESSION_KEY_REFRESH_TOKEN] = (
            response.json()['refresh_token']
        )
        return redirect(self.redirect_url)
