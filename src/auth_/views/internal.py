from micro.jango.permissions import IsInternal
from micro.jango.serializers import IdSerializer
from micro.jango.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response

from auth_.serializers import AuthSerializer
from auth_.services import AuthService


class InternalViewSet(BaseViewSet):
    permission_classes = (IsInternal,)
    authentication_classes = ()

    @post(url_path="list")
    def list_(self, request):
        auths = AuthService.list_auths()
        resp = dict(auths=AuthSerializer(auths, many=True).data)
        return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="create")
    def create_(self, request):
        data = request.data.copy()
        serializer = AuthSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email, password = serializer.extract("email", "password")
            auth = AuthService.create_auth(email, password)
            resp = dict(auth=AuthSerializer(auth).data)
            return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="lookup")
    def lookup(self, request):
        data = request.data.copy()
        serializer = IdSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            auth = AuthService.get_auth(serializer.pop("id"))  # TODO: exists
            resp = dict(auth=IdSerializer(auth).data)
            return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="info")
    def info(self, request):
        data = request.data.copy()
        serializer = IdSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            auth = AuthService.get_auth(serializer.pop("id"))
            resp = dict(auth=AuthSerializer(auth).data)
            return Response(data=resp, status=status.HTTP_200_OK)

    @post(url_path="destroy")
    def destroy_(self, request):
        data = request.data.copy()
        serializer = IdSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            AuthService.destroy_auth(data.pop("id"))
            return Response(status=status.HTTP_200_OK)
