import pytest

from tests.auth import AuthTestBase


class TestVerify(AuthTestBase):
    @pytest.mark.parametrize("token", ("", "random"))
    def test_verify_invalid(self, base_client, token):
        token = "invalid"
        base_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.client_request(self.VERIFY_URL, client=base_client, status=403, ok=False)

    def test_verify_authenticated(self, base_client):
        user, token = self.login_auth()
        base_client.credentials(HTTP_AUTHORIZATION=f"Token {token.access}")
        self.client_request(self.VERIFY_URL, client=base_client, status=200, ok=True)
