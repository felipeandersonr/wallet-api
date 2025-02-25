from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_session

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm, session: Session = Depends(get_session)) -> dict:
    pass
