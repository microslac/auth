import pytest

from tests.auth import AuthTestBase
from tests.factories import AuthFactory


class TestSignup(AuthTestBase):
    @pytest.mark.parametrize("email", ("email@example", "email", "@example.com"))
    def test_signup_invalid_email(self, email):
        data = dict(email=email, password="password")
        resp = self.client_request(self.SIGNUP_URL, data=data, base=True, status=400, ok=False)
        assert resp.error == "invalid"

    @pytest.mark.parametrize("password", ("", "passwor", "p" * 129))
    def test_signup_invalid_password(self, password):
        data = dict(email="email@example.com", password=password)
        resp = self.client_request(self.SIGNUP_URL, data=data, base=True, status=400, ok=False)
        if not password:
            assert resp.error == "blank"
        elif len(password) < 8:  # min
            assert resp.error == "min_length"
        elif len(password) > 128:  # max
            assert resp.error == "max_length"

    def test_signup_already_exists(self):
        auth = AuthFactory()
        data = dict(email=auth.email, password="password")
        resp = self.client_request(self.SIGNUP_URL, data=data, base=True, status=400, ok=False)
        assert resp.error == "already_exists"

    def test_signup_success(self, base_client):
        data = dict(email="email@example.com", password="password")
        resp = self.client_request(self.SIGNUP_URL, data=data, base=True, status=200, ok=True)
        assert getattr(resp, "refresh", None) is None
        assert resp.access is not None
