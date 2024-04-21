from tests.base import ApiTestBase
from types import SimpleNamespace

from tests.factories import AuthFactory
from auths.models import Auth


class AuthTestBase(ApiTestBase):
    URL = "/auth"
    LOGIN_URL = f"{URL}/login"
    SIGNUP_URL = f"{URL}/signup"
    OBTAIN_URL = f"{URL}/obtain"
    VERIFY_URL = f"{URL}/verify"
    REFRESH_URL = f"{URL}/refresh"

    def mock_auth(self) -> tuple[Auth, str]:
        auth = AuthFactory()
        password = auth.password
        auth.set_password(auth.password)
        auth.save()
        return auth, password

    def login_auth(self) -> tuple[Auth, SimpleNamespace]:
        auth, password = self.mock_auth()
        data = dict(email=auth.email, password=password)
        response = self.base_client.post(self.LOGIN_URL, data=data, format="json")
        self.base_client.credentials(HTTP_AUTHORIZATION=f"Token {response.data['access']}")
        token = self.objectify(response.data)
        return auth, token
