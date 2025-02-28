from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.controller.login import LoginController
from app.database import get_session
from app.shcemas.login import TokenPublic

router = APIRouter()


@router.post("/login", response_model=TokenPublic)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)) -> TokenPublic:
    token = LoginController(session).login(form_data)

    return token


@router.post("/logout/{user_id}")
def logout(user_id: int, session: Session = Depends(get_session)):
    result = LoginController(session).logout(user_id)

    return result
