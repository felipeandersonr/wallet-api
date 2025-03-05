from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controller.wallet import WalletController
from app.database import get_session
from app.exceptions.permissions import permission_exceptions
from app.models.user import User
from app.security import get_current_user
from app.shcemas.wallet import WalletPublic


router = APIRouter()


@router.get("/wallet/{user_id}", response_model=WalletPublic)
def get_wallet(user_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> WalletPublic:
    if user_id != user.id:    
        permission_exceptions.not_enought_permission()
 
    wallet = WalletController(session).get_wallet_by_user_id(user_id=user_id)

    return wallet


@router.post("wallet/{user_id}", response_model=WalletPublic)
def create_wallet(user_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> WalletPublic:
    if user_id != user.id:    
        permission_exceptions.not_enought_permission()

    wallet = WalletController(session).create_wallet_by_user_id(user_id=user_id)

    return wallet
