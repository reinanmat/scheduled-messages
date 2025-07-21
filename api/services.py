from sqlalchemy.orm import Session
from common.dapr_client import schedule_message_via_actor
from common.logger import logger

from api.models import ScheduledMessage
from api.schemas import MessageCreate
from common.schemas import ScheduledMessageFull


async def create_scheduled_message(db: Session, msg: MessageCreate):
    try:
        message = ScheduledMessage(
            content=msg.content,
            scheduled_time=msg.scheduled_time
        )
        db.add(message)
        db.commit()
        db.refresh(message)

        message_schema = ScheduledMessageFull.model_validate(message)
        await schedule_message_via_actor(message_schema)

        return message
    except Exception as e:
        logger.error(f"[API] Error: failed to create a message: {e}")
        raise


def get_message_by_id(db: Session, msg_id: int):
    return db.query(ScheduledMessage).filter(ScheduledMessage.id == msg_id).first()


def get_all_messages(db: Session):
    return db.query(ScheduledMessage).order_by(ScheduledMessage.scheduled_time).all()


def send_scheduled_message(db: Session, msg):
    try:
        msg.sent = True
        db.commit()
        db.refresh(msg)
        logger.info(f"[API] Message: \"{msg.content}\" was sent successfully!")
    except Exception as e:
        logger.error(f"[API] Failed to send a message: {msg}, error: {e}")
        raise e
