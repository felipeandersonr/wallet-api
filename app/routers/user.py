from http import HTTPStatus

from fastapi import APIRouter

from app.utils.annotated import GetSession
from app.controller.user import UserController
from app.shcemas.user import UserPublic, UserSchema


router = APIRouter(prefix="/users", tags=["user"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user_data: UserSchema, session: GetSession):
    new_user = UserController(session).create_user(user_data)

    return new_user
