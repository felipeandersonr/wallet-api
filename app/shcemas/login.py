from pydantic import BaseModel


class TokenPublic(BaseModel):
    nickname: str
    password: str
