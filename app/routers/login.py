from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.controller.login import LoginController
from app.database import get_session
from app.models.user import User
from app.security import get_current_user
from app.shcemas.login import TokenPublic
from app.shcemas.generic import Message
from app.exceptions.permissions import permission_exceptions


router = APIRouter(prefix="/auth", tags=["token"])


@router.post("/login", response_model=TokenPublic)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)) -> TokenPublic:
    token = LoginController(session).login(form_data)

    return token


@router.delete("/logout/{user_id}", response_model=Message)
def logout(user_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    if user.id != user_id:
        permission_exceptions.not_enought_permission()
    
    LoginController(session).logout(user_id)

    message = {"message": "Authorization token deleted"}

    return message
