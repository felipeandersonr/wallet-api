from sqlalchemy.orm import Session

from app.models.friendship import Friendship


def create_test_friendship(session: Session, user_id: int, friend_id: int, status: str = "pending") -> Friendship:
    friendship = Friendship(
        status=status,
        user_id=user_id,
        friend_id=friend_id
    )
    
    session.add(friendship)
    session.commit()

    return friendship
