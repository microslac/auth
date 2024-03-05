from micro.jango.tests import UnitTestBase

from auth_.constants import AuthSource
from auth_.models import Auth


class TestAuthModel(UnitTestBase):
    def test_create_user(self):
        auth = Auth(email="email@example.com", password="password")

        assert auth.uuid
        assert auth.id.startswith("A")
        assert auth.email == auth.email
        assert auth.password is not None
        assert auth.source == AuthSource.SLAC
