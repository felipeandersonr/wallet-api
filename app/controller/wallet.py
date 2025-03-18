from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy import exists, select
from app.controller.base_controller import BaseController
from app.models.wallet import Wallet


class WalletController(BaseController):
    def get_wallet_by_user_id(self, user_id: int):
        wallet = self.session.scalar(select(Wallet).where(Wallet.user_id == user_id))

        if not wallet:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, 
                detail="User wallet not founded"
            )
        
        return wallet
        
    
    def create_wallet_by_user_id(self, user_id: int) -> Wallet:
        exists_wallet = self.session.scalar(select(exists().where(Wallet.user_id == user_id)))

        if exists_wallet:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, 
                detail="User already has a wallet"
            )
    
        new_wallet = Wallet(
            user_id=user_id, 
            balance=0
        )

        self.session.add(new_wallet)
        self.session.commit()

        return new_wallet
    

    def deposit_wallet_by_user_id(self, user_id: int, amount: float) -> Wallet:
        if amount <= 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, 
                detail="Amount must be greater than 0"
            )
        
        wallet = self.get_wallet_by_user_id(user_id=user_id)

        wallet.balance += amount

        self.session.commit()

        return wallet


    def withdraw_wallet_by_user_id(self, user_id: int, amount: float) -> Wallet:    
        if amount <= 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, 
                detail="Amount must be greater than 0"
            )
    
        wallet = self.get_wallet_by_user_id(user_id=user_id)

        if wallet.balance < amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, 
                detail="Insufficient balance"
            )
        
        wallet.balance -= amount

        self.session.commit()

        return wallet
    