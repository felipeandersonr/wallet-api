from datetime import date
from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy import or_, select
from app.controller.base_controller import BaseController
from app.models.transaction import Transaction
from app.models.user import User
from app.models.wallet import Wallet
from app.utils.annotated import FilterPage


class TransactionController(BaseController):
    def get_transactions(self, 
                         pagination: FilterPage, 
                         user_id: int | None = None, 
                         end_date: date | None = None, 
                         start_date: date | None = None,
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
