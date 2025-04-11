from http import HTTPStatus
from fastapi import APIRouter

from app.utils.annotated import CurrentUser, GetRedisAPI, GetSession
from app.controller.wallet import WalletController
from app.shcemas.wallet import WalletPublic


router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/", response_model=WalletPublic)
def get_wallet(session: GetSession, user: CurrentUser, redis_api_cache: GetRedisAPI) -> WalletPublic:
    wallet = WalletController(session=session).get_wallet_by_user_id_with_cache(
        user_id=user.id, 
        redis_api_cache=redis_api_cache
    )

    return wallet


@router.post("/create/", status_code=HTTPStatus.CREATED, response_model=WalletPublic)
def create_wallet(session: GetSession, user: CurrentUser) -> WalletPublic:
    wallet = WalletController(session).create_wallet_by_user_id(user_id=user.id)

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
    