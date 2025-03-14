from http import HTTPStatus
from fastapi import APIRouter

from app.shcemas.friendship import FriendshipPublic
from app.utils.annotated import CurrentUser, GetSession


router = APIRouter(prefix="/friendship", tags=["friendship"])


@router.get("/{user_id}", status_code=HTTPStatus.OK , response_model=list[FriendshipPublic])
def get_user_friendship(user_id: int, session: GetSession, user: CurrentUser):
    pass


@router.post("/request", status_code=HTTPStatus.CREATED, response_model=FriendshipPublic)
def create_friendship_request(session: GetSession, user: CurrentUser):
    pass
