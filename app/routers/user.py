from http import HTTPStatus

from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.utils.annotated import CurrentUser, FilterPage, GetSession
from app.controller.user import UserController
from app.shcemas.user import UserPublic, UserSchema


router = APIRouter(prefix="/users", tags=["user"])


@router.post("/create", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user_data: UserSchema, session: GetSession):
    new_user = UserController(session).create_user(user_data)

    return new_user


class GetUsersFiltersModel(BaseModel):
    nickname: str = None
    pagination: FilterPage | None = None


@router.post("/", status_code=HTTPStatus.OK, response_model=list[UserPublic])
def get_users(session: GetSession, user: CurrentUser, filters: GetUsersFiltersModel = Body(None)):
    if filters is None:
        filters = GetUsersFiltersModel()

    users = UserController(session=session).get_users(
        nickname=filters.nickname, 
        pagination=filters.pagination,
    )

    return users
