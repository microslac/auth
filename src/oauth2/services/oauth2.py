import re
from base64 import b64encode
from datetime import timedelta
from urllib.parse import urlencode

from authlib.integrations.django_client import DjangoOAuth2App
from micro.jango.exceptions import ApiException
from micro.jango.services import BaseService
from rest_framework.request import Request

from auths.exceptions.auth import DuplicatedSocialEmail
from auths.services.auth import AuthService
from auths.simplejwt.tokens import RefreshToken
from oauth2.services.client import oauth, providers
from oauth2.services.social import SocialInfo


class Oauth2Service(BaseService):
    def __init__(self, source: str, request: Request):
        if source not in providers:
            raise ApiException(error="invalid_provider")

        self.client: DjangoOAuth2App = oauth.create_client(source)
        self.request = request
        self.source = source

    def create_authorization_url(self) -> str:
        origin = self._get_request_origin()
        redirect_uri = self._build_redirect_uri()
        rv: dict = self.client.create_authorization_url(redirect_uri)
        self.client.save_authorize_data(self.request, origin=origin, **rv)
        return rv["url"]

    def create_authorized_url(self) -> str:
        redirect_uri = self._build_redirect_uri()
        claims_options = self._get_claims_options()
        token = self.client.authorize_access_token(
            self.request,
            redirect_uri=redirect_uri,
            claims_options=claims_options,
        )
        state_data = self.client.framework.state_data  # once

        userinfo = token.get("userinfo", {})
        if not userinfo:
            userinfo = self.client.userinfo(token=token)

        social = SocialInfo.factory(source=self.source)
        email, data = social.get_social_data(userinfo)

        try:
            auth = AuthService.get_or_create_social_auth(email=email, source=self.source, data=data)
        except DuplicatedSocialEmail:
            error_url = "{}/{}?{}".format(state_data.get("origin"), "signin", "error=duplicated_social_email")
            return error_url

        app_token = RefreshToken.for_user(auth)
        app_token.set_exp(lifetime=timedelta(minutes=1))
        encoded_refresh = b64encode(str(app_token).encode())
        encoded_params = urlencode({"_r": encoded_refresh})
        authorized_url = "{}/{}?{}".format(state_data.get("origin"), "signin", encoded_params)

        return authorized_url

    def _build_redirect_uri(self) -> str:
        redirect_uri: str = self.request.build_absolute_uri()
        redirect_uri: str = redirect_uri.replace("authorize", "callback", 1)
        redirect_uri: str = re.sub(r"\?.*$", "", redirect_uri)
        return redirect_uri

    def _get_request_origin(self) -> str:
        return self.request.META.get("HTTP_ORIGIN")

    def _get_claims_options(self) -> dict:
        if self.source == "linkedin":
            return {"nonce_supported": False}
        return {}
