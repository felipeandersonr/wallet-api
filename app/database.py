import redis

from datetime import datetime
from typing import Protocol, TypeVar
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Session

from app.settings import settings


class SQLAlchemyModel(Protocol):
    __tablename__: str
    id: int
    created_at: datetime
    updated_at: datetime


table_registry = registry()


T = TypeVar("T", bound=SQLAlchemyModel)


engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


def get_client_redis_api() -> redis.Redis:
    redis_api_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )
    
    return redis_api_client
