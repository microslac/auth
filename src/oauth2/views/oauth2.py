from django.shortcuts import redirect
from micro.jango.views import BaseViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from oauth2.services.oauth2 import Oauth2Service


class Oauth2ViewSet(BaseViewSet):
    authentication_classes = ()
    permission_classes = ()

    @action(methods=["GET"], detail=False)
    def authorize(self, request: Request, source: str = ""):
        service = Oauth2Service(source=source, request=request)
        authorization_url = service.create_authorization_url()
        resp = dict(authorization_url=authorization_url)
        return Response(resp, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def callback(self, request: Request, source: str = ""):
        service = Oauth2Service(source=source, request=request)
        authorized_url = service.create_authorized_url()
        return redirect(authorized_url)
