from pydantic import BaseModel


class ChatPublic(BaseModel):
    id: int
    user_1_id: int
    user_2_id: int
