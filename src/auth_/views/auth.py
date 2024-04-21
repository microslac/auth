from micro.jango.views import BaseViewSet, post
from rest_framework import status
from rest_framework.response import Response

from auth_.serializers import LoginSerializer, ObtainSerializer, RefreshSerializer, SignupSerializer
from auth_.services import AuthService

public = dict(permission_classes=(), authentication_classes=())


class AuthViewSet(BaseViewSet):
    @post(url_path="signup", **public)
    def signup(self, request):
        data = request.data.copy()
        serializer = SignupSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email, password = serializer.extract("email", "password")
            access, _ = AuthService.signup(email=email, password=password)
            return Response(dict(access=access), status=status.HTTP_200_OK)

    @post(url_path="login", **public)
    def login(self, request):
        data = request.data.copy()
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            email, password = serializer.extract("email", "password")
            access, _ = AuthService.login(email=email, password=password)
            return Response(dict(access=access), status=status.HTTP_200_OK)

    @post(url_path="consume", **public)
    def consume(self, request):
        data = request.data.copy()
        serializer = RefreshSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            access, _ = AuthService.refresh(serializer.validated_data["refresh"])
            return Response(dict(access=access), status=status.HTTP_200_OK)

    @post(url_path="verify", **public)
    def verify(self, request):
        is_verified = AuthService.verify(request=request)
        if is_verified:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @post(url_path="obtain")
    def obtain(self, request):
        auth = request.user
        data = request.data.copy()
        serializer = ObtainSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            team_id = serializer.pop("team")
            access, refresh = AuthService.obtain(auth, team_id)
            return Response(dict(access=access, refresh=refresh), status=status.HTTP_200_OK)

    @post(url_path="refresh")
    def refresh(self, request):
        data = request.data.copy()
        serializer = RefreshSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            access, rotated_refresh = AuthService.refresh(serializer.validated_data["refresh"])
            return Response(dict(access=access, refresh=rotated_refresh), status=status.HTTP_200_OK)
