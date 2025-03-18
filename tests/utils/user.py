from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.fake_data import faker_data
from app.utils.safety import hash_password


def create_test_user(session: Session, password: str = "senha_do_usuario123") -> User:
    hashed_password = hash_password(password)

    name = faker_data.name()
    nickname = faker_data.pystr()
    email = faker_data.email()

    new_user = User(
        name=name,
        email=email,
        nickname=nickname,
        hashed_password=hashed_password
    )

    session.add(new_user)
    session.commit()

    return new_user


def create_many_test_user(session: Session, many_times: int = 3) -> list[User]:
    users = []

    for _ in range(many_times):
        new_user = create_test_user(
            session=session, 
            password=faker_data.password()
        )

        users.append(new_user)

    return users
