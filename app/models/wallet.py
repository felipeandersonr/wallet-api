from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import table_registry


@table_registry.mapped_as_dataclass
class Wallet:
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    balance: Mapped[float] = mapped_column(nullable=False, default=0)

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
