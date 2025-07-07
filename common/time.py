from datetime import datetime, timezone
from typing import Union


def ensure_utc_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_timestamp_ms(dt: Union[datetime, str]) -> int:
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    dt = ensure_utc_aware(dt)
    return int(dt.timestamp() * 1000)


def from_timestamp_ms(ts: int) -> datetime:
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc)


def serialize_scheduled_message(message_id: str, content: str, scheduled_time: Union[datetime, str]) -> dict:
    dt = ensure_utc_aware(scheduled_time if isinstance(scheduled_time, datetime) else datetime.fromisoformat(scheduled_time))
    return {
        "message_id": message_id,
        "content": content,
        "scheduled_time": to_timestamp_ms(dt),
        "scheduled_time_iso": dt.isoformat()
    }
