from http import HTTPStatus
from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.controller.friendship import FriendshipController
from app.shcemas.friendship import FriendshipPublic
from app.utils.annotated import CurrentUser, GetSession


router = APIRouter(prefix="/friendship", tags=["friendship"])


class GetFriendshipModel(BaseModel):
    user_id: int
    is_active: bool = True
    pedding_status: bool = True
    accepted_status: bool = True
    rejected_status: bool = True


@router.post("/{user_id}", status_code=HTTPStatus.OK , response_model=list[FriendshipPublic])
def get_user_friendship(user_id: int, session: GetSession, user: CurrentUser, filters: GetFriendshipModel = Body(None)):
    if filters is None:
        filters = GetFriendshipModel()

    friendships = FriendshipController(session=session).get_friendships(
        user_id=user_id,
        accepted_status=filters.accepted_status,
        rejected_status=filters.rejected_status,
        pedding_status=filters.pedding_status,
        is_active=filters.is_active
    )   

    return friendships


@router.post("/request/{friend_id}", status_code=HTTPStatus.CREATED, response_model=FriendshipPublic)
def create_friendship_request(session: GetSession, user: CurrentUser, friend_id: int):
    new_friendship = FriendshipController(session=session).create_friendship_request(
        friend_id=friend_id,
        current_user_id=user.id
    )

    return new_friendship


@router.post("/accept/{friendship_id}", status_code=HTTPStatus.OK, response_model=FriendshipPublic)
def accept_friendship_request(session: GetSession, user: CurrentUser, friendship_id: int):
    accepted_friendship = FriendshipController(session=session).accept_friendship_request(friendship_id=friendship_id)

    return accepted_friendship


@router.post("/reject/{friendship_id}", status_code=HTTPStatus.OK, response_model=FriendshipPublic)
def reject_friendship_request(session: GetSession, user: CurrentUser, friendship_id: int):
    rejected_friendship = FriendshipController(session=session).reject_friendship_request(friendship_id=friendship_id)

    return rejected_friendship
