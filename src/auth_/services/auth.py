from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.db import IntegrityError
from django.db.models import QuerySet
from micro.jango.exceptions import ApiException
from micro.jango.services import BaseService
from micro.services.registry import UsersService
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from auth_.auth.authentication import JWTAuthentication
from auth_.constants import AuthSource
from auth_.exceptions.auth import DuplicatedSocialEmail
from auth_.models import Auth
from auth_.simplejwt.tokens import AppRefreshToken


class AuthService(BaseService):
    @classmethod
    def signup(cls, email: str, password: str, *, data: dict = None) -> tuple[str, str]:
        data = dict(fullname=email.split("@")[0].lower())
        auth = cls.create_auth(email, password, data=data)
        token = RefreshToken.for_user(auth)
        access, refresh = str(token.access_token), str(token)  # noqa
        return access, refresh

    @classmethod
    def login(cls, email: str, password: str) -> tuple[str, str]:
        auth = authenticate(email=email, password=password)
        if auth is None:
            raise ApiException(error="invalid_credentials")
        token = RefreshToken.for_user(auth)
        access, refresh = str(token.access_token), str(token)  # noqa
        return access, refresh

    @classmethod
    def verify(cls, request: Request) -> bool:
        res = JWTAuthentication().authenticate(request)
        return bool(res)

    @classmethod
    def refresh(cls, refresh: str) -> tuple[str, str]:
        try:
            token = RefreshToken(refresh)  # noqa
            access = str(token.access_token)
            token.blacklist()
            token.set_jti()
            token.set_exp()
            token.set_iat()
            return access, str(token)
        except TokenError as exc:
            raise ApiException(error="invalid_refresh_token") from exc

    @classmethod
    def obtain(cls, auth: Auth, team_id: str) -> tuple[str, str]:
        # TODO: make access token live shorter
        lookup_data = dict(team=team_id, auth=auth.id)
        user = UsersService.post("/internal/lookup", data=lookup_data, key="user")
        token = AppRefreshToken.for_app_user(auth, team_id=team_id, user_id=user.pop("id"))
        access, refresh = str(token.access_token), str(token)  # noqa
        return access, refresh

    @classmethod
    def create_auth(cls, email: str, password: str, *, source: str = "", data: dict = None) -> Auth:
        try:
            validate_email(email)
            source = source or AuthSource.SLAC
            data = data or {}
            data.update(fullname=email.split("@", 1).pop(0))
            auth = Auth(email=email, password=password, source=source, data=data)
            auth.set_password(password)
            auth.save()
            return auth
        except IntegrityError as exc:
            raise ApiException(error="already_exists") from exc

    @classmethod
    def get_or_create_social_auth(cls, email: str, source: str, data: dict) -> Auth:
        try:
            validate_email(email)
            auth, created = Auth.objects.get_or_create(email=email, source=source, defaults={"data": data})
            if created:
                auth.set_unusable_password()
                auth.save()
            return auth
        except IntegrityError as exc:
            raise DuplicatedSocialEmail(error="duplicated_social_email") from exc

    @classmethod
    def get_auth(cls, auth_id: str) -> Auth:
        return Auth.objects.get(id=auth_id)

    @classmethod
    def list_auths(cls) -> QuerySet[Auth]:
        return Auth.objects.all()

    @classmethod
    def destroy_auth(cls, auth_id: str):
        auth = Auth.objects.get(id=auth_id)
        auth.delete()
