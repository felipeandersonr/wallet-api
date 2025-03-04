from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_authenticator import UserAuthenticator


def create_test_user_authenticator(session: Session, user: User) -> UserAuthenticator:
    new_authenticator = UserAuthenticator(
        user_id=user.id
    )

    new_authenticator.generate()
    new_authenticator.use()

    session.add(new_authenticator)
    session.commit()

    return new_authenticator
