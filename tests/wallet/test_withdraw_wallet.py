from http import HTTPStatus
from tests.base_test_class import BaseTest


class TestWithdrawWallet(BaseTest):
    router_url = f"/wallet/withdraw"
    
    
    def test_withdraw_wallet(self, session, client, common_user_authenticated, wallet_from_common_user):
        amount = 100
        wallet_from_common_user.balance = 1000
        older_wallet_balance = wallet_from_common_user.balance

        session.commit()
        session.refresh(wallet_from_common_user)

        response = self.request_client_post(
            client=client, 
            router_url=f"{self.router_url}/{amount}",
            authorization_token=common_user_authenticated.token,
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json()["balance"] == older_wallet_balance - amount
        assert response.json()["user_id"] == wallet_from_common_user.user_id
    

    def test_withdraw_wallet_with_negative_amount(self, session, client, common_user_authenticated):
        amount = -1

        response = self.request_client_post(
            client=client, 
            authorization_token=common_user_authenticated.token,
            router_url=f"{self.router_url}/{amount}"
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["error"] == "Amount must be greater than 0"


    def test_withdraw_wallet_with_zero_amount(self, session, client, common_user_authenticated):
        amount = 0

        response = self.request_client_post(
            client=client, 
            authorization_token=common_user_authenticated.token,
            router_url=f"{self.router_url}/{amount}"
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["error"] == "Amount must be greater than 0"
    

    def test_withdraw_wallet_with_insufficient_balance(self, session, client, common_user_authenticated, wallet_from_common_user):
        amount = 1000
        wallet_from_common_user.balance = 0

        session.commit()
        session.refresh(wallet_from_common_user)

        response = self.request_client_post(
            client=client, 
            authorization_token=common_user_authenticated.token,
            router_url=f"{self.router_url}/{amount}"
        )
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["error"] == "Insufficient balance"
