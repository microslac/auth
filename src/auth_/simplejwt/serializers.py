from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user, context: dict = None) -> Token:
        token = super().get_token(user)
        if context:
            for key, value in context.items():
                if value:
                    token[key] = value
        return token
