from django.shortcuts import redirect
from micro.jango.views import BaseViewSet
from rest_framework.decorators import action
from rest_framework.request import Request

from oauth2.socials.context import SocialContext
from oauth2.socials.strategy import SocialStrategy


class Oauth2ViewSet(BaseViewSet):
    authentication_classes = ()
    permission_classes = ()

    @action(methods=["GET"], detail=False)
    def authorize(self, request: Request, social_name: str = ""):
        strategy = SocialStrategy.factory(social_name, request=request)
        context = SocialContext(strategy=strategy)
        authorization_url, state = context.get_authorization_url()
        return redirect(authorization_url)

    @action(methods=["GET"], detail=False)
    def callback(self, request: Request, social_name: str = ""):
        strategy = SocialStrategy.factory(social_name, request=request)
        context = SocialContext(strategy=strategy)
        authorized_url = context.create_authorized_response()
        return redirect(authorized_url)
