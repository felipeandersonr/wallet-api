from pydantic import BaseModel

from app.utils.annotated import FilterPage


class FriendshipPublic(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: str
    is_active: bool


class GetFriendshipModel(BaseModel):
    is_active: bool = True
    user_id: int | None = None
    peding_status: bool = True
    accepted_status: bool = True
    rejected_status: bool = True
    pagination: FilterPage | None = None
    