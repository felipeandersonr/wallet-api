from datetime import datetime
from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import table_registry


@table_registry.mapped_as_dataclass
class Chat:
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_1_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_2_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    deleted_by_user_1: Mapped[bool] = mapped_column(default=False)
    deleted_by_user_2: Mapped[bool] = mapped_column(default=False)
    
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
