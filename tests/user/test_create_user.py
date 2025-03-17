from http import HTTPStatus

from sqlalchemy import select

from app.models.user import User
from tests.base_test_class import BaseTest


class TestCreateUser(BaseTest):
    def test_create_user_success(self, client, session):
        response = self.request_client_post(
            client=client, 
            router_url="/users/create", 
            json_data={
                "name": "James",
                "password": "123",
                "nickname": "james_",
                "email": "james@gmail.com"
            }
        )

        self.request_client_post

        james_user_id = session.scalar(select(User.id).where(User.nickname == "james_"))

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "name": "James",
            "id": james_user_id,
            "nickname": "james_",
            "email": "james@gmail.com"
        }


    def test_create_user_with_invalid_email(self, client):
        response = self.request_client_post(
            client=client, 
            router_url="/users/create",
            json_data={
                "name": "Jorge",
                "password": "123",
                "nickname": "jor_",
                "email": "jorge@.com"
            }
        )

        assert response.status_code == 422
        assert response.json()["error"] == "Validation Error"


    def test_create_user_with_invalid_name(self, client):
        response = self.request_client_post(
            client=client, 
            router_url="/users/create",
            json_data={
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


    def test_create_user_with_invalid_nickname(self, client):
        response = self.request_client_post(
            client=client, 
            router_url="/users/create",
            json_data={
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

    
    def test_create_user_with_email_already_exists(self, client, common_user):
        common_user_email = common_user.email

        response = self.request_client_post(
            client=client,
            router_url="/users/create",
            json_data={
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


    def test_create_user_with_nickname_already_exists(self, client, common_user):
        common_user_nickname = common_user.nickname

        response = self.request_client_post(
            client=client,
            router_url="/users/create",
            json_data={
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
