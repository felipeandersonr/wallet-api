from http import HTTPStatus
from app.models.friendship import Friendship
from app.utils.fake_data import get_random_nonexistent_id
from tests.base_test_class import BaseTest
from tests.utils.friendship import create_test_friendship


class TestRejectFriendship(BaseTest):
    router = "/friendship/reject"

    def test_reject_friendship_success(self, session, client, common_user_authenticated, common_user, another_user):
        friendship_request = create_test_friendship(
            session=session,
            user_id=common_user.id,
            friend_id=another_user.id,
            status="pending"
        )

        assert friendship_request.status == "pending"

        response = self.request_client_post(
            client=client,
            router_url=f"{self.router}/{friendship_request.id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json["status"] == "rejected"

    def test_reject_friendship_with_nonexistent_friendship_id(self, session, client, common_user_authenticated):
        nonexistent_friendship_id = get_random_nonexistent_id(session=session, model_class=Friendship)

        response = self.request_client_post(
            client=client,
            router_url=f"{self.router}/{nonexistent_friendship_id}",
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response_json["error"] == "Friendship request not found"
