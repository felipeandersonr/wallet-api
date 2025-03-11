from datetime import date
from http import HTTPStatus
from fastapi import APIRouter, Body
from pydantic import BaseModel

from app.utils.annotated import CurrentUser, FilterPage, GetSession
from app.controller.transaction import TransactionController
from app.shcemas.transaction import TransactionPublic
from app.exceptions.permissions import permission_exceptions


router = APIRouter(prefix="/transaction", tags=["transaction"])


class TransactionFiltersModel(BaseModel):
    only_incoming: bool = False
    only_outgoing: bool = False
    end_date: date | None = None
    start_date: date | None = None
    pagination: FilterPage | None = None


@router.post("/{user_id}", status_code=HTTPStatus.OK, response_model=list[TransactionPublic])
def get_transactions(user_id: int, user: CurrentUser, session: GetSession, filters: TransactionFiltersModel = Body(None)):
    if user.id != user_id:
        permission_exceptions.not_enought_permission()

    if filters is None:
        filters = TransactionFiltersModel()

    transactions = TransactionController(session).get_transactions(
        user_id=user_id, 
        end_date=filters.end_date, 
        start_date=filters.start_date,
        pagination=filters.pagination, 
        only_incoming_transactions=filters.only_incoming, 
        only_outgoing_transactions=filters.only_outgoing
    )

    return transactions
