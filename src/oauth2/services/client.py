from typing import Dict, Optional

from authlib.integrations import django_client as client
from django.core.cache import cache

from api.settings import env


class DjangoOAuth2App(client.DjangoOAuth2App):
    def parse_id_token(self, token, nonce, claims_options=None, leeway=120):
        if claims_options and claims_options.get("nonce_supported") is False:
            claims_options.pop("nonce_supported")
            nonce = None
        super().parse_id_token(token, nonce, claims_options, leeway)


class DjangoIntegration(client.DjangoIntegration):
    _state_data: Optional[Dict]

    @property
    def state_data(self):
        value = self._state_data
        self._state_data = None
        return value

    def clear_state_data(self, session, state):
        self._state_data = super().get_state_data(session, state)
        super().clear_state_data(session, state)


class OAuth(client.OAuth):
    framework_integration_cls = DjangoIntegration
    oauth2_client_cls = DjangoOAuth2App


oauth = OAuth(cache=cache)

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "email profile openid"},
)

oauth.register(
    name="github",
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    userinfo_endpoint="https://api.github.com/user",
    client_kwargs={"scope": "user"},
)

linkedin = oauth.register(
    name="linkedin",
    server_metadata_url="https://www.linkedin.com/oauth/.well-known/openid-configuration",
    access_token_params={"client_secret": env.str("OAUTH2_LINKEDIN_CLIENT_SECRET", default="")},
    client_kwargs={"scope": "email profile openid"},
)

providers = ("google", "github", "linkedin")
