from sqlalchemy import create_engine
from sqlalchemy.orm import registry, Session

from app.settings import settings

db_url = settings.DATABASE_URL
table_registry = registry()
engine = create_engine(db_url)


def get_session():
    with Session(engine) as session:
        yield session
