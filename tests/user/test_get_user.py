from http import HTTPStatus
from tests.base_test_class import BaseTest
from tests.utils.user import create_many_test_user


class TestGetUsers(BaseTest):
    def test_get_users_success(self, client, common_user_authenticated, session):
        new_users = create_many_test_user(session=session, many_times=2)
        
        response = self.request_client_post(
            client=client, 
            router_url="/users",
            authorization_token=common_user_authenticated.token
        )

        assert response.status_code == HTTPStatus.OK

        response_json = response.json()

        assert len(response_json) == 2 + 1 # created 2 users in tests and the common user (2 + 1)

        for user in response_json:
            assert user["id"]
            assert user["name"]
            assert user["email"]
            assert user["nickname"]


    def test_get_users_with_pagination(self, client, session, common_user_authenticated):
        new_users = create_many_test_user(session=session, many_times=5)
        
        response = self.request_client_post(
            client=client, 
            router_url="/users",
            authorization_token=common_user_authenticated.token, 
            json_data={
                "pagination": {
                    "offset": 0, 
                    "limit": 3
                }
            }
        )

        assert len(response.json()) == 3
        assert response.status_code == HTTPStatus.OK


    def test_get_users_with_invalid_pagination(self, client, common_user_authenticated):
        response = self.request_client_post(
            client=client, 
            router_url="/users",
            authorization_token=common_user_authenticated.token, 
            json_data={
                "pagination": {
                    "offset": -1,  # invalid offset
                    "limit": 3
                }
            }
        )

        response_json = response.json()

        assert response_json["error"] == "Validation Error"
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert response_json["details"] == "Value error, limit and offset must be non-negative integers"


    def test_get_only_friends_users(self, client):
        pass


    def test_get_users_by_nickname(self, client):
        pass


    def test_get_only_friends_users_by_nickname(self, client):
        pass
