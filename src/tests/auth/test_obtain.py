import jwt
from micro.services.registry import UsersService
from micro.utils import utils

from tests.auth import AuthTestBase


class TestObtain(AuthTestBase):
    def test_obtain_success(self, mocker):
        team_id, user_id = utils.shortid("T"), utils.shortid("U")
        data = dict(team=team_id, user=user_id)

        auth, token = self.login_auth()
        mocker.patch.object(UsersService, "post", return_value=dict(id=user_id))
        resp = self.client_request(self.OBTAIN_URL, data=data, base=True, status=200, ok=True)

        assert resp.ok is True
        assert resp.access is not None
        assert resp.refresh is not None

        token_data = jwt.decode(jwt=resp.access, options={"verify_signature": False})
        assert token_data["aid"] == auth.id
        assert token_data["tid"] == team_id
        assert token_data["uid"] == user_id
