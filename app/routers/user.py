from http import HTTPStatus

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.controller.user import UserController
from app.database import get_session
from app.shcemas.user import UserPublic, UserSchema


router = APIRouter()


@router.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user_data: UserSchema, session: Session = Depends(get_session)):
    new_user = UserController(session).create_user(user_data)

    return new_user
