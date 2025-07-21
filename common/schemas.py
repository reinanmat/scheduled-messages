from pydantic import BaseModel
from datetime import datetime

class ScheduledMessageFull(BaseModel):
    id: int
    content: str
    scheduled_time: datetime
    sent: bool = False
    created_at: datetime

    class Config:
        from_attributes = True
