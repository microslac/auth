from micro.jango.serializers import BaseModelSerializer, BaseSerializer
from rest_framework import serializers

from auth_.models import Auth


class SignupSerializer(BaseSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, min_length=8, max_length=128)


class LoginSerializer(BaseSerializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, min_length=8, max_length=128)


class RefreshSerializer(BaseSerializer):
    refresh = serializers.CharField(required=True, allow_blank=False)


class ObtainSerializer(BaseSerializer):
    team = serializers.CharField(required=True, allow_blank=False)


class AuthSerializer(BaseModelSerializer):
    email = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False, write_only=True)

    class Meta:
        model = Auth
        fields = ("id", "email", "password", "source", "data")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        extra_data = data.pop("data", {})
        data.update(extra_data)
        return data
