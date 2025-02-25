from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, exists
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_authenticator import UserAuthenticator
from app.utils.safety import verify_password, generate_random_token


class LoginController:
    def __init__(self, session: Session):
        self.session = session

    def login(self, user_form_data: OAuth2PasswordRequestForm) -> dict:
        user_hashed_password, user_id = self.session.scalar(
            select(User.hashed_password, User.id)
            .where(User.nickname == user_form_data.username)
        )

        user_password_match = verify_password(password=user_form_data.password, hashed_password=user_hashed_password)

        if not user_id or not user_password_match:
            exception = HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Incorrect nick or password"
            )

            raise exception

        new_user_authenticator = UserAuthenticator(
            user_id=user_id
        )

        # generate token
        new_user_authenticator.generate()

        # use token
        new_user_authenticator.use()

        self.session.add(new_user_authenticator)
        self.session.commit()

        token = {"access_token": new_user_authenticator.token, "token_type": "bearer"}

        return token
