import pytest

from tests.auth import AuthTestBase


class TestLogin(AuthTestBase):
    @pytest.mark.parametrize("password", ["", "short"])
    def test_login_invalid_password(self, base_client, password):
        data = dict(email="email@example.com", password=password)
        resp = self.client_request(self.LOGIN_URL, data=data, base=True, status=400, ok=False)

        if not password:
            assert resp.error == "blank"
        elif len(password) < 8:
            assert resp.error == "min_length"

    @pytest.mark.parametrize("field", ("email", "password"))
    def test_login_invalid_credentials(self, base_client, field):
        auth, password = self.mock_auth()
        if field == "email":
            data = dict(email="nonexistent@example.com", password=password)
        else:
            data = dict(email=auth.email, password="wrong-password")

        resp = self.client_request(self.LOGIN_URL, data=data, base=True, status=400, ok=False)
        assert resp.error == "invalid_credentials"

    def test_login_success(self, base_client):
        auth, password = self.mock_auth()
        data = dict(email=auth.email, password=password)
        resp = self.client_request(self.LOGIN_URL, data=data, base=True, status=200, ok=True)
        assert getattr(resp, "refresh", None) is None
        assert resp.access is not None
