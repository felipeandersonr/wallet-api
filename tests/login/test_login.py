from http import HTTPStatus

from app.models.user import User
from app.utils.safety import hash_password


def test_login_success():
    pass


def test_login_with_user_dont_exist(client):
    pass


def test_login_with_incorrect_nickname(client, common_user):
    # common user password is 'senha_do_usuario123'
    user_password = "senha_do_usuario123"

    response = client.post(
        "/login", 
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
        "/login", 
        data={
            "username": common_user.nickname, 
            "password": user_password
        }
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_json["status"] == "Failed"
    assert response_json["error"] == "Incorrect nick or password"
