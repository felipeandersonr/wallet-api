from http import HTTPStatus

from tests.utils.user import create_test_user
from tests.utils.wallet import create_test_wallet
from tests.base_test_class import BaseTest


class TestCreateWallet(BaseTest):
    def test_create_wallet_success(self, client, common_user_authenticated):
        response = self.request_client_post(
            client=client,
            router_url=f"/wallet/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response_json["balance"] == 0
        assert response.status_code == HTTPStatus.CREATED
        assert response_json["user_id"] == common_user_authenticated.user_id


    def test_create_wallet_with_user_already_has_a_wallet(self, client, session, common_user_authenticated):
        # create new wallet and relate to common_user
        create_test_wallet(session=session, user_id=common_user_authenticated.user_id)

        response = self.request_client_post(
            client=client,
            router_url=f"/wallet/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.CONFLICT
        assert response_json["error"] == "User already has a wallet"


    def test_create_wallet_to_another_user(self, client, session, common_user_authenticated):
        other_user = create_test_user(session)
        
        response = self.request_client_post(
            client=client,
            router_url=f"/wallet/{other_user.id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response_json["error"] == "Not enough permissions"
