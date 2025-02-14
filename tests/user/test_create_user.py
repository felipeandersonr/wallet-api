from http import HTTPStatus


def test_create_user_success(client):
    response = client.post(
        "/users",
        json={
            "name": "James",
            "password": "123",
            "email": "james@gmail.com"
        }
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "name": "James",
        "email": "james@gmail.com"
    }


def test_create_user_with_invalid_email(client):
    response = client.post(
        "/users",
        json={
            "name": "Jorge",
            "password": "123",
            "email": "jorge@.com"
        }
    )

    assert response.status_code == 422
    assert response.json()["error"] == "validation error"
