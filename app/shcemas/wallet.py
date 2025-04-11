from pydantic import BaseModel


class WalletPublic(BaseModel):
    id: int
    user_id: int
    balance: float


    class Config:
        from_attributes = True
