from http import HTTPStatus
from tests.utils.user import create_test_user
from tests.utils.wallet import create_test_wallet


def test_create_transaction_success(client, session, common_user_authenticated, wallet_from_common_user):
    another_user = create_test_user(session=session)
    wallet_from_another_user = create_test_wallet(session=session, user_id=another_user.id)

    response = client.post(
        "/transaction", 
        json={""}
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.CREATED


def test_create_transaction_to_non_existent_user(client, session, common_user_authenticated):
    pass


def test_create_transaction_with_insufficient_balance_in_wallet(client, session, common_user_authenticated):
    pass


def test_create_transaction_to_me(client, session, common_user_authenticated):
    pass

