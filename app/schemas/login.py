from pydantic import BaseModel


class TokenPublic(BaseModel):
    token_type: str
    access_token: str
