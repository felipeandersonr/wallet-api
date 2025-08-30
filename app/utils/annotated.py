from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

from database import get_session
from models.user import User
from security import get_current_user
from shcemas.generic import FilterPagination, get_filter_pagination


GetSession = Annotated[Session, Depends(get_session)]

CurrentUser = Annotated[User, Depends(get_current_user)]

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

FilterPage = Annotated[FilterPagination, Depends(get_filter_pagination)]
