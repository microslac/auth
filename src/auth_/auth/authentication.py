from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from django.conf import settings
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken, Token

from auth_.models import Auth


class BaseAuthentication(authentication.BaseAuthentication, ABC):
    keyword = "Token"
    auth_model = Auth

    def validate_auth_header(self, request: Request) -> Optional[List[bytes]]:
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid {token} header. No credentials provided.")
            raise AuthenticationFailed(format_lazy(msg, token=self.keyword))
        elif len(auth) > 2:
            msg = _("Invalid {token} header. Token string should not contain spaces.")
            raise AuthenticationFailed(format_lazy(msg, token=self.keyword))
        return auth

    def authenticate_header(self, request: Request):
        return self.keyword

    def decode_auth_data(self, auth: List[bytes]) -> Optional[str]:
        if auth:
            try:
                token = auth[1].decode()
            except UnicodeError:
                msg = _("Invalid {token} header. Token string should not contain invalid characters.")
                raise AuthenticationFailed(format_lazy(msg, token=self.keyword))
            return token

    def authenticate(self, request: Request) -> Optional[Tuple[Auth, str]]:
        auth = self.validate_auth_header(request)
        token = self.decode_auth_data(auth)
        if token:
            return self.authenticate_credentials(token, request)

    @abstractmethod
    def authenticate_credentials(self, token: str, request: Request) -> Tuple[Auth, str]:
        pass


class JWTAuthentication(BaseAuthentication):
    keyword = "Token"

    def authenticate_credentials(self, raw_token: str, request: Request = None) -> Tuple[Auth, str]:
        validated_token = self.get_validated_token(raw_token)
        return self.get_auth(validated_token), str(validated_token)

    def get_validated_token(self, raw_token) -> Token:
        try:
            return AccessToken(raw_token)
        except TokenError as e:
            raise InvalidToken(
                {
                    "detail": _("Given token not valid for any token type"),
                    "messages": [
                        {
                            "token_class": AccessToken.__name__,
                            "token_type": AccessToken.token_type,
                            "message": e.args[0],
                        }
                    ],
                }
            )

    def get_auth(self, validate_token: Token) -> Auth:
        try:
            aid_claim = settings.SIMPLE_JWT["USER_ID_CLAIM"]
            auth_id = validate_token[aid_claim]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable auth identification"))

        try:
            auth = self.auth_model.objects.get(id=auth_id)
        except self.auth_model.DoesNotExist:
            raise AuthenticationFailed(_("Auth not found"), code="auth_not_found")

        if not auth.is_active:
            raise AuthenticationFailed(_("Auth is inactive"), code="auth_inactive")

        return auth
