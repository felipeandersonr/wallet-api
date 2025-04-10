from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

from app.utils.annotated import FilterPage


class TransactionPublic(BaseModel):
    id: int
    value: float
    created_at: datetime
    sender_wallet_id: int
    destination_wallet_id: int
 

    model_config = ConfigDict(from_attributes=True)


class TransactionFiltersModel(BaseModel):
    only_incoming: bool = False
    only_outgoing: bool = False
    end_date: date | None = None
    start_date: date | None = None
    pagination: FilterPage | None = None


class CreteTransactionFiltersModel(BaseModel):
    value: float
    destination_user_id: int
