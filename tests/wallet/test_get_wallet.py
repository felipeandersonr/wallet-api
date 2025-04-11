from http import HTTPStatus

from tests.base_test_class import BaseTest
from tests.utils.wallet import create_test_wallet


class TestGetWallet(BaseTest):
    def test_get_wallet_by_user_id(self, client_with_redis, session, common_user_authenticated, override_redis):
        # create new wallet and relate to common_user
        create_test_wallet(session=session, user_id=common_user_authenticated.user_id)

        response = self.request_client_get(
            client=client_with_redis,
            router_url=f"/wallet/",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json["user_id"] == common_user_authenticated.user_id

