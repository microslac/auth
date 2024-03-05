from tests.internal import InternalTestBase


class TestCreateAuth(InternalTestBase):
    def test_create_auth_success(self):
        data = dict(email="user@example.com", password="password")
        resp = self.client_request(f"{self.URL}/create", data=data, internal=True, status=200, ok=True)

        assert resp.auth.id.startswith("A")
        assert resp.auth.email == data["email"]
        assert resp.auth.fullname == data["email"].split("@", 1).pop(0)
