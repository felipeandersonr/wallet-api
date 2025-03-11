from http import HTTPStatus

from tests.utils.transaction import create_many_test_transaction, create_test_transaction
from tests.utils.user import create_test_user
from tests.utils.wallet import create_test_wallet


def test_get_transaction_success(client, session, wallet_from_common_user, common_user_authenticated):
    # buscar varias transacoes realizadas por um usuario com paginacao

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

    response = client.get(
        f"/transaction/{common_user_authenticated.user_id}", 
        headers={"Authorization": f"Bearer {common_user_authenticated.token}"}
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


def test_get_transactions_with_pagination(client, session, common_user_authenticated, wallet_from_common_user):
    another_user = create_test_user(session=session)
    wallet_from_another_user = create_test_wallet(session=session, user_id=another_user.id)

    transactions_common_user_to_another_user = create_many_test_transaction(
        many_times=5,
        session=session, 
        sender_wallet_id=wallet_from_common_user.id, 
        destination_wallet_id=wallet_from_another_user.id
    )

    response = client.get(
        f"/transaction/{common_user_authenticated.user_id}?offset=0&limit=3", 
        headers={"Authorization": f"Bearer {common_user_authenticated.token}"}
    )

    response_json = response.json()

    assert len(response_json) == 3
    assert response.status_code == HTTPStatus.OK


def test_get_incoming_transactions(client, session, wallet_from_common_user, common_user_authenticated):
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

    response = client.get(
        f"/transaction/{common_user_authenticated.user_id}?only_incoming=true", 
        headers={"Authorization": f"Bearer {common_user_authenticated.token}"}
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.OK

    for transaction in response_json:
        assert transaction["sender_wallet_id"] != wallet_from_common_user.id 
        assert transaction["destination_wallet_id"] == wallet_from_common_user.id 


def test_get_outgoing_transactions(client, session, common_user_authenticated, wallet_from_common_user):
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

    response = client.get(
        f"/transaction/{common_user_authenticated.user_id}?only_outgoing=true", 
        headers={"Authorization": f"Bearer {common_user_authenticated.token}"}
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.OK

    for transaction in response_json:
        assert transaction["sender_wallet_id"] == wallet_from_common_user.id 
        assert transaction["destination_wallet_id"] != wallet_from_common_user.id 


def test_get_incoming_and_outgoing_transactions_filters(client, session, wallet_from_common_user, common_user_authenticated):
    response = client.get(
        f"/transaction/{common_user_authenticated.user_id}?only_incoming=true&only_outgoing=true", 
        headers={"Authorization": f"Bearer {common_user_authenticated.token}"}
    )

    response_json = response.json()

    assert response_json["status"] == "Failed"
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_json["error"] == "You can only request incoming or outgoing transactions at a time, not both"


def test_get_transactions_in_specific_datetime_range(client):
    # todo: fazer o campo de filtro relacionado a datetime range (criado entre o espaco de tempo selecionado pelo usuario)
    
    pass


def test_get_transactions_with_invalid_pagination(client, common_user_authenticated):
    response = client.get(
        f"/transaction/{common_user_authenticated.user_id}?offset=0&limit=-1", 
        headers={"Authorization": f"Bearer {common_user_authenticated.token}"}
    )

    response_json = response.json()

    assert response_json["error"] == "Validation Error"
    assert response_json["details"] == "Value error, limit and offset must be non-negative integers"


def test_get_transactions_without_permission(client):
    # buscar transacoes de outro usuario

    pass
