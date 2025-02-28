import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.main import app
from app.database import table_registry, get_session
from app.models.user import User
from app.utils.fake_data import fake_data
from app.utils.safety import hash_password


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


# user fixtures
@pytest.fixture
def common_user(session) -> User:
    user_password = "senha_do_usuario123"
    hashed_password = hash_password(user_password)

    name = fake_data.name()
    nickname = fake_data.pystr()
    email = fake_data.email()

    new_user = User(
        name=name,
        email=email,
        nickname=nickname,
        hashed_password=hashed_password
    )

    session.add(new_user)
    session.commit()

    return new_user
