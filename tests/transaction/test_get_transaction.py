from datetime import datetime
from http import HTTPStatus

from app.utils.fake_data import faker_data
from tests.utils.transaction import create_many_test_transaction, create_test_transaction
from tests.utils.user import create_test_user
from tests.utils.wallet import create_test_wallet
from tests.base_test_class import BaseTest


class TestGetTransaction(BaseTest):
    def test_get_transaction_success(self, client, session, wallet_from_common_user, common_user_authenticated):
        another_user = create_test_user(session=session)
        wallet_from_another_user = create_test_wallet(session=session, user_id=another_user.id)

        transactions_common_user_to_another_user = create_many_test_transaction(
            many_times=2,
            session=session, 
            sender_wallet_id=wallet_from_common_user.id, 
            destination_wallet_id=wallet_from_another_user.id
        )

        transactions_another_user_to_common_user = create_many_test_transaction(
            many_times=2,
            session=session, 
            sender_wallet_id=wallet_from_another_user.id, 
            destination_wallet_id=wallet_from_common_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=f"/transaction/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert len(response_json) == 4
        
        for transaction in response_json:
            assert transaction["id"]
            assert transaction["value"]
            assert transaction["created_at"]
            assert transaction["sender_wallet_id"]
            assert transaction["destination_wallet_id"]
            assert transaction["destination_wallet_id"] == wallet_from_common_user.id or transaction["sender_wallet_id"] == wallet_from_common_user.id


    def test_get_transactions_with_pagination(self, client, session, common_user_authenticated, wallet_from_common_user):
        another_user = create_test_user(session=session)
        wallet_from_another_user = create_test_wallet(session=session, user_id=another_user.id)

        transactions_common_user_to_another_user = create_many_test_transaction(
            many_times=5,
            session=session, 
            sender_wallet_id=wallet_from_common_user.id, 
            destination_wallet_id=wallet_from_another_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=f"/transaction/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token,
            json_data={
                "pagination": {
                    "offset": 0, 
                    "limit": 3
                }
            }
        )

        response_json = response.json()

        assert len(response_json) == 3
        assert response.status_code == HTTPStatus.OK


    def test_get_incoming_transactions(self, client, session, wallet_from_common_user, common_user_authenticated):
        another_user = create_test_user(session=session)
        wallet_from_another_user = create_test_wallet(session=session, user_id=another_user.id)

        transaction_common_user_to_another_user = create_test_transaction(
            value=100,
            session=session, 
            sender_wallet_id=wallet_from_common_user.id, 
            destination_wallet_id=wallet_from_another_user.id
        )

        transactions_another_user_to_common_user = create_many_test_transaction(
            session=session, 
            sender_wallet_id=wallet_from_another_user.id, 
            destination_wallet_id=wallet_from_common_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=f"/transaction/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token,
            json_data={
                "only_incoming": True
            }
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK

        for transaction in response_json:
            assert transaction["sender_wallet_id"] != wallet_from_common_user.id 
            assert transaction["destination_wallet_id"] == wallet_from_common_user.id 


    def test_get_outgoing_transactions(self, client, session, common_user_authenticated, wallet_from_common_user):
        another_user = create_test_user(session=session)
        wallet_from_another_user = create_test_wallet(session=session, user_id=another_user.id)

        transaction_common_user_to_another_user = create_test_transaction(
            value=150,
            session=session, 
            sender_wallet_id=wallet_from_common_user.id, 
            destination_wallet_id=wallet_from_another_user.id
        )

        transactions_another_user_to_common_user = create_many_test_transaction(
            session=session, 
            sender_wallet_id=wallet_from_another_user.id, 
            destination_wallet_id=wallet_from_common_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=f"/transaction/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token,
            json_data={
                "only_outgoing": True
            }
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK

        for transaction in response_json:
            assert transaction["sender_wallet_id"] == wallet_from_common_user.id 
            assert transaction["destination_wallet_id"] != wallet_from_common_user.id 


    def test_get_incoming_and_outgoing_transactions_filters(self, client, common_user_authenticated):
        response = self.request_client_post(
            client=client,
            router_url=f"/transaction/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token,
            json_data={
                "only_incoming": True, 
                "only_outgoing": True
            }
        )

        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response_json["error"] == "You can only request incoming or outgoing transactions at a time, not both"


    def test_get_transactions_in_specific_datetime_range(self, client, session, common_user_authenticated, wallet_from_common_user):
        another_user = create_test_user(session=session)
        wallet_from_another_user = create_test_wallet(session=session, user_id=another_user.id)

        start_datetime_range = datetime(year=2020, month=1, day=10)
        end_datetime_range = datetime(year=2020, month=2, day=14)

        transactions = create_many_test_transaction(
            many_times=3,
            session=session, 
            sender_wallet_id=wallet_from_another_user.id, 
            destination_wallet_id=wallet_from_common_user.id
        )

        select_transactions = [transactions[0], transactions[1]]

        for selected_transaction in select_transactions:
            selected_transaction.created_at = faker_data.date_between(start_date=start_datetime_range, end_date=end_datetime_range)

            session.commit()
            session.refresh(selected_transaction)

        response = self.request_client_post(
            client=client,
            router_url=f"/transaction/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token,
            json_data={
                "start_date": str(start_datetime_range),
                "end_date": str(end_datetime_range)
            }
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK

        for transaction in response_json:
            assert transaction["created_at"] >= str(start_datetime_range)
            assert transaction["created_at"] <= str(end_datetime_range)


    def test_get_transactions_with_invalid_pagination(self, client, common_user_authenticated):
        response = self.request_client_post(
            client=client,
            router_url=f"/transaction/{common_user_authenticated.user_id}",
            authorization_token=common_user_authenticated.token,
            json_data={
                "pagination": {
                    "offset": 0, 
                    "limit": -1
                }
            }
        )

        response_json = response.json()

        assert response_json["error"] == "Validation Error"
        assert response_json["details"] == "Value error, limit and offset must be non-negative integers"


    def test_get_transactions_without_permission(self, client, session, common_user_authenticated):
        another_user = create_test_user(session=session)

        response = self.request_client_post(
            client=client,
            router_url=f"/transaction/{another_user.id}",
            authorization_token=common_user_authenticated.token
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json()["error"] == "Not enough permissions"
