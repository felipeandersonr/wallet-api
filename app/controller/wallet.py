import json

from http import HTTPStatus
from fastapi import HTTPException
from redis import Redis
from sqlalchemy import exists, select

from app.controller.base_controller import BaseController
from app.models.wallet import Wallet
from app.shcemas.wallet import WalletPublic


class WalletController(BaseController):
    def get_wallet_by_user_id(self, user_id: int) -> Wallet:
        wallet = self.session.scalar(select(Wallet).where(Wallet.user_id == user_id))

        if not wallet:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, 
                detail="User wallet not founded"
            )
        
        return wallet


    def get_wallet_by_user_id_with_cache(self, user_id: int, redis_api_cache: Redis) -> Wallet | WalletPublic:
        cache_key = f"wallet:{user_id}"
        cached_wallet = redis_api_cache.get(cache_key)

        if cached_wallet:
            wallet_data = json.loads(cached_wallet)
            wallet = WalletPublic(**wallet_data)
            
            return wallet

        wallet = self.get_wallet_by_user_id(user_id=user_id)
        
        wallet_data = {"id": wallet.id, "user_id": wallet.user_id, "balance": wallet.balance}        
        redis_api_cache.setex(cache_key, 3600, json.dumps(wallet_data))
        
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
    