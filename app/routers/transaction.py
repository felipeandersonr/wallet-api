from http import HTTPStatus
from fastapi import APIRouter

from app.utils.annotated import CurrentUser, FilterPage, GetSession
from app.controller.transaction import TransactionController
from app.shcemas.transaction import TransactionPublic
from app.exceptions.permissions import permission_exceptions


router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=TransactionPublic)
def create_transaction(user: CurrentUser, session: GetSession):
    pass


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=list[TransactionPublic])
def get_transactions(user_id: int, 
                     user: CurrentUser, 
                     session: GetSession, 
                     pagination: FilterPage, 
                     only_incoming: bool = False, 
                     only_outgoing: bool = False):
    
    if user.id != user_id:
        permission_exceptions.not_enought_permission()

    transactions = TransactionController(session).get_transactions(
        user_id=user_id, 
        pagination=pagination, 
        only_incoming_transactions=only_incoming, 
        only_outgoing_transactions=only_outgoing
    )

    return transactions
