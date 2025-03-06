from sqlalchemy.orm import Session

from app.models.wallet import Wallet


def create_test_wallet(session: Session, user_id: int) -> Wallet:
    new_wallet = Wallet(
        user_id=user_id, 
        balance=0
    )

    session.add(new_wallet)
    session.commit()

    return new_wallet
