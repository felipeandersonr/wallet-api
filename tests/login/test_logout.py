from http import HTTPStatus

from tests.utils.user import create_test_user
from tests.utils.user_authenticator import create_test_user_authenticator
from tests.base_test_class import BaseTest


class TestLogout(BaseTest):
    def test_logout_success(self, client, common_user_authenticated):
        response = self.request_client_delete(
            client=client,
            router_url=f"/auth/logout/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json["message"] == "Authorization token deleted"


    def test_logout_with_no_permission_user(self, client, session, common_user_authenticated):
        new_user = create_test_user(session)
        new_user_authenticated = create_test_user_authenticator(session, new_user)

        response = self.request_client_delete(
            client=client,
            router_url=f"/auth/logout/{common_user_authenticated.user_id}",
            authorization_token=new_user_authenticated.token
        )

        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_json["error"] == "Not enough permissions"
