from pydantic import BaseModel, field_validator
from datetime import datetime

from common.time import ensure_utc_aware


class MessageCreate(BaseModel):
    content: str
    scheduled_time: datetime

    @field_validator('scheduled_time')
    def ensure_aware_utc(cls, time: datetime) -> datetime:
        return ensure_utc_aware(time)


class MessageOut(BaseModel):
    id: int
    content: str
    scheduled_time: datetime
    sent: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
