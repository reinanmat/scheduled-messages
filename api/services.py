from sqlalchemy.orm import Session
from common.logger import logger

from api.models import ScheduledMessage
from api.schemas import MessageCreate
from api.dapr_client import publish_message_scheduled


def create_scheduled_message(db: Session, msg: MessageCreate):
    try:
        message = ScheduledMessage(
            content=msg.content,
            scheduled_time=msg.scheduled_time
        )
        db.add(message)
        db.commit()
        db.refresh(message)

        publish_message_scheduled(message)

        return message
    except Exception as e:
        logger.info(f"Error: failed to create a message: {e}")
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
        logger.info(f"Message: \"{msg.content}\" was sent successfully!")
    except Exception as e:
        logger.error(f"Failed to send a message: {msg}, error: {e}")
        raise e
