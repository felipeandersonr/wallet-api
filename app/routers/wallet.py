from http import HTTPStatus
from fastapi import APIRouter

from app.utils.annotated import CurrentUser, GetSession
from app.controller.wallet import WalletController
from app.exceptions.permissions import permission_exceptions
from app.shcemas.wallet import WalletPublic


router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/{user_id}", response_model=WalletPublic)
def get_wallet(user_id: int, session: GetSession, user: CurrentUser) -> WalletPublic:
    if user_id != user.id:    
        permission_exceptions.not_enought_permission()
 
    wallet = WalletController(session).get_wallet_by_user_id(user_id=user_id)

    return wallet


@router.post("/{user_id}", status_code=HTTPStatus.CREATED, response_model=WalletPublic)
def create_wallet(user_id: int, session: GetSession, user: CurrentUser) -> WalletPublic:
    if user_id != user.id:    
        permission_exceptions.not_enought_permission()

    wallet = WalletController(session).create_wallet_by_user_id(user_id=user_id)

    return wallet


@router.post("/deposit/{amount}", status_code=HTTPStatus.OK, response_model=WalletPublic)
def deposit_wallet(session: GetSession, user: CurrentUser, amount: float) -> WalletPublic:
    wallet = WalletController(session).deposit_wallet_by_user_id(
        user_id=user.id, 
        amount=amount
    )

    return wallet


@router.post("/withdraw/{amount}", status_code=HTTPStatus.OK, response_model=WalletPublic)
def withdraw_wallet(session: GetSession, user: CurrentUser, amount: float) -> WalletPublic:
    wallet = WalletController(session).withdraw_wallet_by_user_id(
        user_id=user.id, 
        amount=amount
    )

    return wallet
    