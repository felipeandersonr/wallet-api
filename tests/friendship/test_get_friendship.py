from sqlalchemy.orm import Session
from http import HTTPStatus

from app.models.user import User
from app.utils.fake_data import get_random_nonexistent_id
from tests.base_test_class import BaseTest
from tests.utils.friendship import create_test_friendship
from tests.utils.user import create_test_user


class TestGetFriendship(BaseTest):
    router = "/friendship"


    def __create_friendship_to_users(self, session: Session, user_1_id: int, user_2_id: int):
        common_user_to_another_user_friendship_request = create_test_friendship(
            session=session,
            user_id=user_1_id,
            friend_id=user_2_id,
            status="pending"
        )

        new_user = create_test_user(
            session=session
        )

        new_user_to_another_user_friendship = create_test_friendship(
            session=session, 
            user_id=new_user.id, 
            friend_id=user_2_id, 
            status="accepted"
        ) 

        common_user_to_new_user_friendship = create_test_friendship(
            session=session,
            user_id=user_1_id,
            friend_id=new_user.id,
            status="rejected"
        )
        
    
    def test_get_friendship_success(self, session, client, common_user_authenticated, another_user):
        self.__create_friendship_to_users(
            session=session,
            user_1_id=common_user_authenticated.user_id,
            user_2_id=another_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=self.router,
            authorization_token=common_user_authenticated.token
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json
        
        for friendship in response_json:
            assert friendship["is_active"] == True
            assert friendship["status"] in ["pending", "accepted", "rejected"]


    def test_get_friendship_with_pagination(self, client, session, common_user_authenticated, another_user):
        self.__create_friendship_to_users(
            session=session,
            user_1_id=common_user_authenticated.user_id,
            user_2_id=another_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=self.router,
            authorization_token=common_user_authenticated.token,
            json_data={
                "pagination": {
                    "offset": 1,
                    "limit": 1
                }
            }
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json
        assert len(response_json) == 1


    def test_get_friendship_with_invalid_pagination(self, client, common_user_authenticated):
        response = self.request_client_post(
            client=client,
            router_url=self.router,
            authorization_token=common_user_authenticated.token,
            json_data={
                "pagination": {
                    "offset": -1,
                    "limit": 1
                }
            }
        )

        response_json = response.json()

        assert response_json["error"] == "Validation Error"
        assert response_json["details"] == "Value error, limit and offset must be non-negative integers"


    def test_get_accepted_friendship(self, client, session, common_user_authenticated, another_user):
        self.__create_friendship_to_users(
            session=session,
            user_1_id=common_user_authenticated.user_id,
            user_2_id=another_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=self.router,
            authorization_token=common_user_authenticated.token,
            json_data={
                "accepted_status": True, 
                "rejected_status": False, 
                "peding_status": False
            }
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json
        
        for friendship in response_json:
            assert friendship["status"] == "accepted"


    def test_get_rejected_friendship(self, client, session, common_user_authenticated, another_user):
        self.__create_friendship_to_users(
            session=session,
            user_1_id=common_user_authenticated.user_id,
            user_2_id=another_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=self.router,
            authorization_token=common_user_authenticated.token,
            json_data={
                "accepted_status": False, 
                "rejected_status": True, 
                "peding_status": False
            }
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json
        
        for friendship in response_json:
            assert friendship["status"] == "rejected"


    def test_get_pending_friendship(self, client, session, another_user, common_user_authenticated):
        self.__create_friendship_to_users(
            session=session,
            user_1_id=common_user_authenticated.user_id,
            user_2_id=another_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=self.router,
            authorization_token=common_user_authenticated.token,
            json_data={
                "accepted_status": False, 
                "rejected_status": False, 
                "peding_status": True
            }
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json
        
        for friendship in response_json:
            assert friendship["status"] == "pending"


    def test_get_friendship_with_nonexistent_user_id(self, client, session, common_user_authenticated):
        nonexistent_user_id = get_random_nonexistent_id(session=session, model_class=User)

        response = self.request_client_post(
            client=client,
            router_url=self.router,
            authorization_token=common_user_authenticated.token,
            json_data={
                "user_id": nonexistent_user_id
            }
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["error"] == "User not found"
    

    def test_get_friendship_by_user_id(self, client, session, common_user_authenticated, another_user):
        user_id = common_user_authenticated.user_id

        self.__create_friendship_to_users(
            session=session,
            user_1_id=user_id,
            user_2_id=another_user.id
        )

        response = self.request_client_post(
            client=client,
            router_url=self.router,
            authorization_token=common_user_authenticated.token, 
            json_data={
                "user_id": user_id
            }
        )

        response_json = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_json
        
        for friendship in response_json:
            assert friendship["is_active"] == True
            assert friendship["user_id"] == user_id or friendship["friend_id"] == user_id
