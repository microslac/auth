import re

import validators
from social_core.backends.oauth import BaseOAuth2
from social_core.utils import handle_http_errors
from social_django.strategy import DjangoStrategy


class DjangoStrategyDeco(DjangoStrategy):
    def build_absolute_uri(self, path=None):
        redirect_uri: str = super().build_absolute_uri(path)
        callback_uri: str = redirect_uri.replace("authorize", "callback", 1)
        callback_uri: str = re.sub(r"\?.*$", "", callback_uri)
        return callback_uri


class Oauth2Deco(BaseOAuth2):
    def __init__(self, *args, **kwargs):
        self._backend: BaseOAuth2 = kwargs.pop("backend")
        super().__init__(*args, **kwargs)

    def auth_url(self):
        return self._backend.auth_url()

    @handle_http_errors
    def get_access_response(self, *args, **kwargs) -> tuple[str, dict]:
        backend = self._backend

        backend.process_error(backend.data)
        state = backend.validate_state()
        data, params = None, None
        if backend.ACCESS_TOKEN_METHOD == "GET":
            params = backend.auth_complete_params(state)
        else:
            data = backend.auth_complete_params(state)

        response = backend.request_access_token(
            backend.access_token_url(),
            data=data,
            params=params,
            headers=backend.auth_headers(),
            auth=backend.auth_complete_credentials(),
            method=backend.ACCESS_TOKEN_METHOD,
        )
        backend.process_error(response)
        return response["access_token"], response

    def get_user_response(self, *args, **kwargs) -> tuple[str, dict]:
        backend = self._backend

        access_token, response = self.get_access_response(backend)
        user_data = backend.user_data(access_token)
        user_details = backend.get_user_details(user_data)
        email = user_details.get("email")
        username = user_details.get("username")
        if not validators.email(email):
            email = f"{username}@{backend.name}.com"  # satisfy user.email
        return email, user_details
