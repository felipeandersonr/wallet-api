from http import HTTPStatus
from fastapi import APIRouter, Body

from app.utils.annotated import CurrentUser, GetSession
from app.controller.transaction import TransactionController
from app.shcemas.transaction import CreteTransactionFiltersModel, TransactionFiltersModel, TransactionPublic
from app.exceptions.permissions import permission_exceptions


router = APIRouter(prefix="/transaction", tags=["transaction"])


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


@router.post("/create/", status_code=HTTPStatus.CREATED, response_model=TransactionPublic)
def create_transaction(session: GetSession, user: CurrentUser, filters: CreteTransactionFiltersModel = Body(...)): 
    new_transaction = TransactionController(session=session).create_transaction(
        value=filters.value,
        sender_user_id=user.id, 
        destination_user_id=filters.destination_user_id
    )

    return new_transaction
