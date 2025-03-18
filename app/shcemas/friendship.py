from pydantic import BaseModel


class FriendshipPublic(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: str
    is_active: bool
