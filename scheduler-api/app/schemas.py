from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    content: str
    scheduled_time: datetime


class MessageOut(BaseModel):
    id: int
    content: str
    scheduled_time: datetime
    sent: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
