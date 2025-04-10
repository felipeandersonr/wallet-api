from pydantic import BaseModel

from app.utils.annotated import FilterPage


class ChatPublic(BaseModel):
    id: int
    user_1_id: int
    user_2_id: int


class GetChatsFiltersModel(BaseModel):
    pagination: FilterPage
    user_nickname: str | None = None
