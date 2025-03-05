from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import table_registry


@table_registry.mapped_as_dataclass
class Transaction:
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    sender_wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)
    destination_wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"), nullable=False)

    value: Mapped[float] 

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        nullable=True,
        onupdate=func.now()
    )
    