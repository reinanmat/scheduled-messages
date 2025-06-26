from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class ScheduledMessage:
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    content: Mapped[str]
    scheduled_time: Mapped[datetime]
    sent: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
