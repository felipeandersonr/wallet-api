from http import HTTPStatus

from sqlalchemy import select

from app.models.user_authenticator import UserAuthenticator


def test_login_success(client, common_user, session):
    # common user password is 'senha_do_usuario123'
    user_password = "senha_do_usuario123"

    response = client.post(
        "/auth/login", 
        data={
            "username": common_user.nickname, 
            "password": user_password
        }
    )

    response_json = response.json()

    common_user_authenticator = session.scalar(
        select(UserAuthenticator)
        .where(UserAuthenticator.user_id == common_user.id and UserAuthenticator.is_active == True)
    )

    assert response.status_code == HTTPStatus.OK
    assert response_json["access_token"]
    assert response_json["token_type"]

    assert common_user_authenticator is not None


def test_login_with_user_does_not_exist(client):
    response = client.post(
        "/auth/login", 
        data={
            "username": "does_not_exist_user_nickname", 
            "password": "123"
        }
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_json["status"] == "Failed"
    assert response_json["error"] == "Incorrect nick or password"

def test_login_with_incorrect_nickname(client, common_user):
    # common user password is 'senha_do_usuario123'
    user_password = "senha_do_usuario123"

    response = client.post(
        "/auth/login", 
        data={
            "username": "incorrect_nickname", 
            "password": user_password
        }
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_json["status"] == "Failed"
    assert response_json["error"] == "Incorrect nick or password"


def test_login_with_incorrect_password(client, common_user):
    # common user password is 'senha_do_usuario123'
    user_password = "incorrect_user_password"
    
    response = client.post(
        "/auth/login", 
        data={
            "username": common_user.nickname, 
            "password": user_password
        }
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_json["status"] == "Failed"
    assert response_json["error"] == "Incorrect nick or password"
