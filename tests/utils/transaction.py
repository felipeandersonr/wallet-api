from random import randint
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def create_test_transaction(session: Session, 
                            sender_wallet_id: int, 
                            destination_wallet_id: int, 
                            value: float) -> Transaction:
    
    new_transaction = Transaction(
        value=value, 
        sender_wallet_id=sender_wallet_id, 
        destination_wallet_id=destination_wallet_id
    )

    session.add(new_transaction)
    session.commit()

    return new_transaction


def create_many_test_transaction(session: Session,
                                sender_wallet_id: int, 
                                destination_wallet_id: int, 
                                many_times: int = 3) -> list[Transaction]:
    
    new_transactions = []

    for _ in range(many_times):
        value = randint(100, 1000)

        new_transaction = create_test_transaction(
            value=value,
            session=session,
            sender_wallet_id=sender_wallet_id, 
            destination_wallet_id=destination_wallet_id
        )

        new_transactions.append(new_transaction)

    return new_transactions
