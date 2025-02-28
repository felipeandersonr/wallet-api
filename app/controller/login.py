from http import HTTPStatus

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.controller.base_controller import BaseController
from app.models.user import User
from app.models.user_authenticator import UserAuthenticator
from app.shcemas.login import TokenPublic
from app.utils.safety import verify_password


class LoginController(BaseController):
    def login(self, user_form_data: OAuth2PasswordRequestForm) -> TokenPublic:
        result = self.session.execute(
            select(User.hashed_password, User.id)
            .where(User.nickname == user_form_data.username)
        ).first() 

        if not result:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Incorrect nick or password"
            )
        
        user_hashed_password, user_id = result 

        user_password_match = verify_password(password=user_form_data.password, hashed_password=user_hashed_password)

        if not user_password_match:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Incorrect nick or password"
            )

        new_user_authenticator = UserAuthenticator(
            user_id=user_id
        )

        # generate token
        new_user_authenticator.generate()

        # use token
        new_user_authenticator.use()

        self.session.add(new_user_authenticator)
        self.session.commit()

        token = TokenPublic(
            token_type="bearer",
            access_token=new_user_authenticator.token
        )

        return token

    def logout(self, user_id: int):
        active_token = self.session.scalar(
            select(UserAuthenticator)
            .where(UserAuthenticator.user_id == user_id and UserAuthenticator.is_active == True)
        )

        active_token.delete()

        self.session.commit()

        return True
