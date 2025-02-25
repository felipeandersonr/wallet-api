from datetime import datetime

from sqlalchemy import func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.database import table_registry


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)

    name: Mapped[str]
    hashed_password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    nickname: Mapped[str] = mapped_column(unique=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        init=False,
        nullable=True,
        onupdate=func.now()
    )
