from http import HTTPStatus
from fastapi import APIRouter, Body

from app.utils.annotated import CurrentUser, GetSession
from app.controller.user import UserController
from app.shcemas.user import GetUsersFiltersModel, UserPublic, UserSchema


router = APIRouter(prefix="/users", tags=["user"])


@router.post("/create", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user_data: UserSchema, session: GetSession):
    new_user = UserController(session).create_user(user_data)

    return new_user


@router.post("/", status_code=HTTPStatus.OK, response_model=list[UserPublic])
def get_users(session: GetSession, user: CurrentUser, filters: GetUsersFiltersModel = Body(None)):
    if filters is None:
        filters = GetUsersFiltersModel()

    users = UserController(session=session).get_users(
        nickname=filters.nickname, 
        pagination=filters.pagination,
    )

    return users
