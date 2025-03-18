from datetime import datetime
from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import table_registry


@table_registry.mapped_as_dataclass
class Friendship:
    __tablename__ = "friendships"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    status: Mapped[str]

    is_active: Mapped[bool] = mapped_column(default=True)

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
