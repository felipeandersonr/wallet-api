from pydantic import BaseModel


class TokenPublic(BaseModel):
    access_token: str
    token_type: str
