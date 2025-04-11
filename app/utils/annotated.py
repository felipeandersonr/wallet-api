import redis

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

from app.database import get_client_redis_api, get_session
from app.models.user import User
from app.security import get_current_user
from app.shcemas.generic import FilterPagination, get_filter_pagination


GetSession = Annotated[Session, Depends(get_session)]

GetRedisAPI = Annotated[redis.Redis, Depends(get_client_redis_api)]

CurrentUser = Annotated[User, Depends(get_current_user)]

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

FilterPage = Annotated[FilterPagination, Depends(get_filter_pagination)]
