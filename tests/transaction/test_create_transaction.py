from http import HTTPStatus
from app.controller.transaction import TransactionController
from app.models.user import User
from app.utils.fake_data import get_random_nonexistent_id
from tests.utils.friendship import create_test_friendship
from tests.utils.user import create_test_user
from tests.utils.wallet import create_test_wallet
from tests.base_test_class import BaseTest


class TestCreateTransaction(BaseTest):
    def test_create_transaction_success(self, client, session, common_user_authenticated, wallet_from_common_user):       
        another_user = create_test_user(session=session)
        wallet_from_another_user = create_test_wallet(session=session, user_id=another_user.id)

        wallet_from_common_user.balance = 1000

        session.commit()
        session.refresh(wallet_from_common_user)

        common_user_another_user_friendship = create_test_friendship(
            session=session,
            user_id=common_user_authenticated.user_id, 
            friend_id=another_user.id,
            status="accepted"
        )

        data = {   
         "value": 150.5, 
         "destination_user_id": another_user.id,
        }

        response = self.request_client_post(
            client=client,
            router_url="/transaction/create/",
            authorization_token=common_user_authenticated.token,
            json_data=data
        )

        response_json = response.json()

        sender_wallet_id = TransactionController(session=session).get_wallet_id_by_user_id(user_id=common_user_authenticated.user_id)
        destination_wallet_id = TransactionController(session=session).get_wallet_id_by_user_id(user_id=data["destination_user_id"])
       
        assert response.status_code == HTTPStatus.CREATED
        assert response_json["id"] 
        assert response_json["created_at"]
        assert response_json["value"] == data["value"]
        assert response_json["sender_wallet_id"] == sender_wallet_id
        assert response_json["destination_wallet_id"] == destination_wallet_id


    def test_create_transaction_to_non_existent_user(self, client, session, common_user_authenticated):
        nonexistent_user_id = get_random_nonexistent_id(session=session, model_class=User)

        response = self.request_client_post(
            client=client,
            router_url="/transaction/create/",
            authorization_token=common_user_authenticated.token,
            json_data={
                "value": 10000, 
                "destination_user_id": nonexistent_user_id
            }
        )

        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response_json["error"] == "User has no wallet"


    def test_create_transaction_when_user_has_no_wallet(self, client, session, common_user_authenticated):
        another_user = create_test_user(session=session)

        response = self.request_client_post(
            client=client,
            router_url="/transaction/create/",
            authorization_token=common_user_authenticated.token,
            json_data={
                "value": 150.5, 
                "destination_user_id": another_user.id,
            }
        )
       
        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response_json["error"] == "User has no wallet"


    def test_create_transaction_with_insufficient_balance_in_wallet(self, client, session, common_user_authenticated, wallet_from_common_user):
        another_user = create_test_user(session=session)
        wallet_from_another_user = create_test_wallet(session=session, user_id=another_user.id)

        wallet_from_common_user.balance = 10

        session.commit()
        session.refresh(wallet_from_common_user)
        
        response = self.request_client_post(
            client=client,
            router_url="/transaction/create/",
            authorization_token=common_user_authenticated.token,
            json_data={
                "value": 100, 
                "destination_user_id": another_user.id,
            }
        )
       
        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response_json["error"] == "Insufficient balance"
        assert response.status_code == HTTPStatus.PAYMENT_REQUIRED


    def test_create_transaction_to_me(self, client, common_user_authenticated):
        response = self.request_client_post(
            client=client,
            router_url="/transaction/create/",
            authorization_token=common_user_authenticated.token,
            json_data={
                "value": 100, 
                "destination_user_id": common_user_authenticated.user_id
            }
        )
       
        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response_json["error"] == "Cannot carry out a transaction for you"
