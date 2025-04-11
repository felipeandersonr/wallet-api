from unittest.mock import patch
import fakeredis
import pytest

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from main import app
from app.database import get_client_redis_api, table_registry, get_session
from app.models.user import User
from tests.utils.user import create_test_user
from tests.utils.user_authenticator import create_test_user_authenticator
from tests.utils.wallet import create_test_wallet


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def client_with_redis(session, override_redis):
    def get_session_override():
        return session
    
    def get_redis_override():
        return override_redis 

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        app.dependency_overrides[get_client_redis_api] = get_redis_override

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


# @pytest.fixture
# def override_redis(monkeypatch):
#     fake_redis = fakeredis.FakeRedis(decode_responses=True)

#     monkeypatch.setattr("app.database.get_client_redis_api", lambda: fake_redis)

#     return fake_redis


@pytest.fixture
def override_redis():
    """Substitui a função get_client_redis_api por um FakeRedis"""
    fake_redis = fakeredis.FakeRedis(decode_responses=True)
    
    # Usando patch é mais confiável do que monkeypatch em alguns casos
    with patch("app.database.get_client_redis_api", return_value=fake_redis):
        yield fake_redis



# user fixtures
@pytest.fixture
def common_user(session) -> User:
    common_user = create_test_user(session=session)
    
    return common_user


@pytest.fixture
def another_user(session) -> User:
    another_user = create_test_user(
        session=session,
        password="another_user_password"
    )
    
    return another_user


# user authenticator fixtures 
@pytest.fixture
def common_user_authenticated(session, common_user):
    common_user_authenticated = create_test_user_authenticator(session, common_user)

    return common_user_authenticated


# wallet
@pytest.fixture
def wallet_from_common_user(session, common_user):
    wallet = create_test_wallet(session=session, user_id=common_user.id)

    return wallet
