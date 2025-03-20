from datetime import date
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy import and_, exists, or_, select

from app.controller.base_controller import BaseController
from app.models.friendship import Friendship
from app.models.transaction import Transaction
from app.models.user import User
from app.models.wallet import Wallet
from app.utils.annotated import FilterPage
from app.exceptions.friendship import friendship_exceptions


class TransactionController(BaseController):
    def get_transactions(self, 
                         user_id: int | None = None, 
                         end_date: date | None = None, 
                         start_date: date | None = None,
                         pagination: FilterPage | None = None, 
                         only_incoming_transactions: bool = False,
                         only_outgoing_transactions: bool = False) -> list[Transaction]:
        
        if only_incoming_transactions and only_outgoing_transactions:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="You can only request incoming or outgoing transactions at a time, not both"
            )
         
        statement = select(Transaction)
        
        if only_outgoing_transactions and not only_incoming_transactions:
            statement = statement.join(Wallet, Transaction.sender_wallet_id == Wallet.id)

        if only_incoming_transactions and not only_outgoing_transactions:
            statement = statement.join(Wallet, Transaction.destination_wallet_id == Wallet.id)

        if user_id:
            if not only_outgoing_transactions and not only_incoming_transactions:
                statement = statement.join(Wallet, or_(Transaction.sender_wallet_id == Wallet.id, Transaction.destination_wallet_id == Wallet.id))

            statement = statement.join(User, Wallet.user_id == User.id).where(User.id == user_id)

        if start_date:
            statement = statement.where(Transaction.created_at >= start_date)

        if end_date:
            statement = statement.where(Transaction.created_at <= end_date)

        if pagination:
            statement = statement.offset(pagination.offset).limit(pagination.limit)

        statement = statement.distinct()

        transactions = self.session.scalars(statement).all()

        return transactions
    

    def get_wallet_id_by_user_id(self, user_id: int) -> int | None:
        wallet_id = self.session.scalar(select(Wallet.id).where(Wallet.user_id == user_id))

        return wallet_id
    

    def check_if_users_are_friends(self, sender_user_id: int, destination_user_id: int) -> bool:
        statement = select(
            exists().select_from(Friendship).where(
                or_(
                    and_(
                        Friendship.user_id == sender_user_id, 
                        Friendship.friend_id == destination_user_id
                    ),

                    and_(
                        Friendship.user_id == destination_user_id, 
                        Friendship.friend_id == sender_user_id
                    )
                ), 

                Friendship.status == "accepted", 
                Friendship.is_active == True
            )
        )

        are_users_friend = self.session.scalar(statement)

        return are_users_friend


    def create_transaction(self, sender_user_id: int, destination_user_id: int, value: float) -> Transaction:
        if sender_user_id == destination_user_id:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Cannot carry out a transaction for you"
            )
        
        sender_wallet = self.session.scalar(select(Wallet).where(Wallet.user_id == sender_user_id))
        destination_wallet_id = self.get_wallet_id_by_user_id(user_id=destination_user_id)    

        if not sender_wallet or not destination_wallet_id:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, 
                detail="User has no wallet"
            )
        
        if sender_wallet.balance < value:
            raise HTTPException(
                detail="Insufficient balance", 
                status_code=HTTPStatus.PAYMENT_REQUIRED
            )
        
        are_users_friends = self.check_if_users_are_friends(
            sender_user_id=sender_user_id,
            destination_user_id=destination_user_id
        )
        
        if not are_users_friends:
            raise friendship_exceptions.friendship_required()
        
        new_transaction = Transaction(
            value=value,
            sender_wallet_id=sender_wallet.id, 
            destination_wallet_id=destination_wallet_id
        )

        self.session.add(new_transaction)
        self.session.commit()

        return new_transaction
    