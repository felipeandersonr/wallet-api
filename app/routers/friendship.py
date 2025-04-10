from http import HTTPStatus
from fastapi import APIRouter, Body

from app.controller.friendship import FriendshipController
from app.shcemas.friendship import FriendshipPublic, GetFriendshipModel
from app.utils.annotated import CurrentUser, GetSession


router = APIRouter(prefix="/friendship", tags=["friendship"])


@router.post("/", status_code=HTTPStatus.OK , response_model=list[FriendshipPublic])
def get_user_friendship(session: GetSession, user: CurrentUser, filters: GetFriendshipModel = Body(None)):
    if filters is None:
        filters = GetFriendshipModel()

    friendships = FriendshipController(session=session).get_friendships(
        user_id=filters.user_id,
        is_active=filters.is_active,
        pagination=filters.pagination,
        peding_status=filters.peding_status,
        accepted_status=filters.accepted_status,
        rejected_status=filters.rejected_status
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
