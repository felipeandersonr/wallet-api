from http import HTTPStatus
from tests.utils.user import create_test_user
from tests.utils.wallet import create_test_wallet


def test_get_wallet_by_user_id(client, session, common_user_authenticated):
    # create new wallet and relate to common_user
    create_test_wallet(session=session, user_id=common_user_authenticated.user_id)

    response = client.get(
        f"/wallet/{common_user_authenticated.user_id}", 
        headers={"Authorization": f"Bearer {common_user_authenticated.token}"}
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert response_json["user_id"] == common_user_authenticated.user_id


def test_get_wallet_of_another_user(client, session, common_user_authenticated):
    other_user = create_test_user(session)
    
    response = client.get(
        f"/wallet/{other_user.id}", 
        headers={"Authorization": f"Bearer {common_user_authenticated.token}"}
    )

    response_json = response.json()

    assert response_json["status"] == "Failed"
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response_json["error"] == "Not enough permissions"
