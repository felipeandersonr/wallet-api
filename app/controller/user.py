from http import HTTPStatus

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from app.models.user import User
from app.shcemas.user import UserPublic, UserSchema
from app.utils.safety import hash_password


class UserController:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data: UserSchema) -> UserPublic:
        email_statement = select(exists().where(User.email == user_data.email))
        nickname_statement = select(exists().where(User.nickname == user_data.nickname))

        if self.session.scalar(email_statement):
            exception = HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="User email already used"
            )

            raise exception

        if self.session.scalar(nickname_statement):
            exception = HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Nickname already used"
            )

            raise exception

        hashed_password = hash_password(user_data.password)

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            nickname=user_data.nickname,
            hashed_password=hashed_password
        )

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)

        logger.info(f"create user {new_user.name}/{new_user.email} in database")

        user_public = UserPublic(
            name=user_data.name,
            email=user_data.email,
            nickname=user_data.nickname
        )

        return user_public
