from tests.factories import AuthFactory
from tests.internal import InternalTestBase


class TestReadUser(InternalTestBase):
    def test_lookup_auth_success(self):
        auth = AuthFactory()
        data = dict(id=auth.id)
        resp = self.client_request(f"{self.URL}/lookup", data=data, internal=True, status=200, ok=True)
        assert resp.auth.id == auth.id

    def test_info_auth_success(self):
        auth = AuthFactory()
        data = dict(id=auth.id)
        resp = self.client_request(f"{self.URL}/info", data=data, internal=True, status=200, ok=True)
        assert resp.auth.id == auth.id
        assert resp.auth.email == auth.email
        assert auth.email.startswith(resp.auth.fullname)
