import pytest
from micro.services.registry import UsersService
from micro.utils.utils import shortid
from rest_framework import status

from tests.auth import AuthTestBase


class TestRefresh(AuthTestBase):
    @pytest.mark.parametrize("refresh", ("", "invalid"))
    def test_refresh_invalid(self, base_client, refresh):
        data = dict(refresh=refresh)
        response = base_client.post(self.REFRESH_URL, data=data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        resp = self.objectify(response.data)
        assert resp.ok is False
        if not refresh:
            assert resp.error == "blank"
        else:
            assert resp.error == "invalid_refresh_token"

    def test_refresh_success(self, mocker):
        self.login_auth()
        team_id, user_id = shortid("T"), shortid("U")
        obtain_data = dict(team=team_id, user=user_id)
        mocker.patch.object(UsersService, "post", return_value=dict(id=user_id))
        obtain = self.client_request(self.OBTAIN_URL, data=obtain_data, base=True)

        data = dict(refresh=obtain.refresh)
        resp = self.client_request(self.REFRESH_URL, data=data, base=True, status=200, ok=True)
        assert resp.access is not None
        assert resp.refresh is not None
