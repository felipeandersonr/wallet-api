from datetime import datetime, timezone

from sqlalchemy import func, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.database import table_registry
from app.utils.safety import generate_random_token


@table_registry.mapped_as_dataclass
class UserAuthenticator:
    __tablename__  = "user_authenticators"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)

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

    def generate(self):
        self.token = generate_random_token()

    def use(self):
        self.updated_at = datetime.now(timezone.utc)

    def delete(self):
        self.is_active = False
