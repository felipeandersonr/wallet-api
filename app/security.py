from http import HTTPStatus
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.user import User
from app.models.user_authenticator import UserAuthenticator


def get_current_user(token: str, session: Session = Depends(get_session)) -> User:
    authenticator = session.scalar(
        select(UserAuthenticator)
        .where(UserAuthenticator.token == token and UserAuthenticator.is_active == True)
    ) 

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED, 
        headers={"WWW-Authenticate": "Bearer"}, 
        detail="Could not validate credentials"
    )

    if not authenticator:
        raise credentials_exception
    
    user = session.scalar(select(User).where(User.id == authenticator.user_id))

    if not user:
        raise credentials_exception
    
    return user
