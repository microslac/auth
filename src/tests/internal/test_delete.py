from auths.models import Auth
from tests.factories import AuthFactory
from tests.internal import InternalTestBase


class TestDeleteUser(InternalTestBase):
    def test_destroy_auth_success(self):
        auth = AuthFactory()
        data = dict(id=auth.id)
        self.client_request(f"{self.URL}/destroy", data=data, internal=True, status=200, ok=True)

        auths = Auth.objects.filter(id=auth.id)
        assert len(auths) == 0
