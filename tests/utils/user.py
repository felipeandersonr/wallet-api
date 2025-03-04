from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.fake_data import fake_data
from app.utils.safety import hash_password


def create_test_user(session: Session) -> User:
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
