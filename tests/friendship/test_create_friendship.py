from http import HTTPStatus
from app.models.user import User
from app.utils.fake_data import get_random_nonexistent_id
from tests.base_test_class import BaseTest
from tests.utils.friendship import create_test_friendship


class TestCreateFriendship(BaseTest):
    def test_create_friendship_request_success(self, client, common_user_authenticated, another_user):
        response = self.request_client_post(
            client=client, 
            router_url=f"/friendship/request/{another_user.id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.CREATED
        assert response_json["status"] == "pending"
        assert response_json["friend_id"] == another_user.id
        assert response_json["user_id"] == common_user_authenticated.id


    def test_create_friendship_request_with_nonexistent_user(self, session, client, common_user_authenticated):
        nonexistent_user_id = get_random_nonexistent_id(session=session, model_class=User)
        
        response = self.request_client_post(
            client=client, 
            router_url=f"/friendship/request/{nonexistent_user_id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response_json["error"] == "User not found"
        assert response.status_code == HTTPStatus.NOT_FOUND


    def test_create_friendship_request_with_me(self, client, common_user_authenticated):
        response = self.request_client_post(
            client=client, 
            router_url=f"/friendship/request/{common_user_authenticated.id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response_json["error"] == "You cannot send a friendship request to yourself"


    def test_create_friendship_request_with_a_friend(self, session, client, common_user_authenticated, another_user, common_user):
        new_friendship = create_test_friendship(
            session=session,
            status="accepted",
            user_id=common_user.id,
            friend_id=another_user.id
        )

        response = self.request_client_post(
            client=client, 
            router_url=f"/friendship/request/{another_user.id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response_json["status"] == "Failed"
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response_json["error"] == "Friendship request already exists"
