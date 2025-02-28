from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.controller.login import LoginController
from app.database import get_session
from app.models.user import User
from app.security import get_current_user
from app.shcemas.login import TokenPublic


router = APIRouter()


@router.post("/login", response_model=TokenPublic)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)) -> TokenPublic:
    token = LoginController(session).login(form_data)

    return token


@router.delete("/logout/{user_id}")
def logout(user_id: int, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if user.id != user_id:
        raise HTTPException(
            detail="Not enough permissions",
            status_code=HTTPStatus.FORBIDDEN 
        )
    
    result = LoginController(session).logout(user_id)

    return result
