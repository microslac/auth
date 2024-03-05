from abc import ABC, abstractmethod
from typing import Type, TypedDict

from django.http import Http404
from micro.patterns.null import Null
from rest_framework.request import Request
from social_core.backends.oauth import BaseOAuth2

from .deco import DjangoStrategyDeco, Oauth2Deco


class UserData(TypedDict):
    email: str
    username: str
    fullname: str
    first_name: str
    last_name: str


class SocialStrategy(ABC):
    name: str
    backend_cls: Type[BaseOAuth2]

    def __init__(self, request: Request):
        self.request = request

    @abstractmethod
    def authorization_url(self) -> tuple[str, str | int]:
        # TODO:
        #   - state:
        #   - PKCE:
        pass

    @abstractmethod
    def user_details(self) -> tuple[str, UserData]:
        pass

    def get_callback_data(self) -> dict:
        return self.request.query_params.copy().dict()

    def get_backend(self) -> Oauth2Deco:
        strategy = DjangoStrategyDeco(storage=None, request=self.request)
        backend = Oauth2Deco(backend=self.backend_cls(strategy=strategy))
        return backend

    @staticmethod
    def factory(name: str, *, request: Request, exc=Http404):
        from .github import GithubStrategy
        from .google import GoogleStrategy

        mapping = {
            GoogleStrategy.name: GoogleStrategy,
            GithubStrategy.name: GithubStrategy,
        }
        strategy_cls = mapping.get(name, Null)
        if not strategy_cls and exc:
            raise exc
        return strategy_cls(request)
