from http import HTTPStatus


def test_create_user_success(client):
    response = client.post(
        "/users",
        json={
            "name": "James",
            "password": "123",
            "nickname": "james_",
            "email": "james@gmail.com"
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "name": "James",
        "nickname": "james_",
        "email": "james@gmail.com"
    }


def test_create_user_with_invalid_email(client):
    response = client.post(
        "/users",
        json={
            "name": "Jorge",
            "password": "123",
            "nickname": "jor_",
            "email": "jorge@.com"
        }
    )

    assert response.status_code == 422
    assert response.json()["error"] == "Validation Error"


def test_create_user_with_invalid_name(client):
    response = client.post(
        "/users",
        json={
            "name": "fe",
            "nickname": "flip",
            "password": "super_flip",
            "email": "flip@hotmail.com"
        }
    )

    response_json = response.json()

    assert response.status_code == 422
    assert response_json["error"] == "Validation Error"
    assert response_json["details"] == "Value error, name or nickname must have at least 3 characters"


def test_create_user_with_invalid_nickname(client):
    response = client.post(
        "/users",
        json={
            "name": "fel",
            "nickname": "f",
            "password": "super_flip",
            "email": "flip@hotmail.com"
        }
    )

    response_json = response.json()

    assert response.status_code == 422
    assert response_json["error"] == "Validation Error"
    assert response_json["details"] == "Value error, name or nickname must have at least 3 characters"

def test_create_user_with_email_already_exists(client, common_user):
    common_user_email = common_user.email

    response = client.post(
        "/users",
        json={
            "name": "felipe",
            "nickname": "flora",
            "password": "super_flip",
            "email": common_user_email
        }
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_json["status"] == "Failed"
    assert response_json["error"] == "User email already used"


def test_create_user_with_nickname_already_exists(client, common_user):
    common_user_nickname = common_user.nickname

    response = client.post(
        "/users",
        json={
            "name": "felipe",
            "password": "super_flip",
            "nickname": common_user_nickname,
            "email": "common_user_email@example.com"
        }
    )

    response_json = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response_json["status"] == "Failed"
    assert response_json["error"] == "Nickname already used"
