from rest_framework_simplejwt.tokens import AuthUser, RefreshToken, Token


class AppRefreshToken(RefreshToken):
    @classmethod
    def for_app_user(cls, auth: AuthUser, team_id: str, user_id: str) -> Token:
        token = cls.for_user(auth)
        token["tid"] = team_id
        token["uid"] = user_id
        return token
