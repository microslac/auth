import base64
from datetime import timedelta
from urllib.parse import urlencode

from auth_.services import AuthService
from auth_.simplejwt.tokens import RefreshToken
from oauth2.socials.strategy import SocialStrategy


class SocialContext:
    def __init__(self, strategy: SocialStrategy):
        self.strategy = strategy

    def get_authorization_url(self) -> tuple[str, str | int]:
        authorization_url, state = self.strategy.authorization_url()
        return authorization_url, state

    def create_authorized_response(self) -> str:
        source = self.strategy.name
        email, data = self.strategy.user_details()
        auth = AuthService.get_or_create_social_auth(email, source=source, data=data)

        token = RefreshToken.for_user(auth)
        token.set_exp(lifetime=timedelta(minutes=1))
        encoded_refresh = base64.b64encode(str(token).encode())
        encoded_params = urlencode({"_r": encoded_refresh})
        login_url = "http://localhost:3000/login"
        authorized_url = f"{login_url}?{encoded_params}"

        return authorized_url
