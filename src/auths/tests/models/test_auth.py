from micro.jango.tests import UnitTestBase

from auths.constants import AuthSource
from auths.models import Auth


class TestAuthModel(UnitTestBase):
    def test_create_user(self):
        auth = Auth(email="email@example.com", password="password")

        assert auth.uuid
        assert auth.id.startswith("A")
        assert auth.email == auth.email
        assert auth.password is not None
        assert auth.source == AuthSource.SLAC
