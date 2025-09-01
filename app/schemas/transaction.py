from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TransactionPublic(BaseModel):
    id: int
    value: float
    created_at: datetime
    sender_wallet_id: int
    destination_wallet_id: int
 

    model_config = ConfigDict(from_attributes=True)
