from http import HTTPStatus

from tests.base_test_class import BaseTest
from tests.utils.user import create_test_user
from tests.utils.wallet import create_test_wallet


class TestGetWallet(BaseTest):
    def test_get_wallet_by_user_id(self, client, session, common_user_authenticated):
        # create new wallet and relate to common_user
        create_test_wallet(session=session, user_id=common_user_authenticated.user_id)

        response = self.request_client_get(
            client=client,
            router_url=f"/wallet/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json["user_id"] == common_user_authenticated.user_id

    def test_get_wallet_of_another_user(self, client, session, common_user_authenticated):
        other_user = create_test_user(session)
        
        response = self.request_client_get(
            client=client,
            router_url=f"/wallet/{other_user.id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_json["error"] == "Not enough permissions"
