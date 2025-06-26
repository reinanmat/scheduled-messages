from sqlalchemy.orm import Session
from app.models import ScheduledMessage
from app.schemas import MessageCreate


def create_message(db: Session, msg: MessageCreate):
    db_msg = ScheduledMessage(
        content=msg.content,
        scheduled_time=msg.scheduled_time
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg


def get_message(db: Session, msg_id: int):
    return db.query(ScheduledMessage).filter(ScheduledMessage.id == msg_id).first()


def list_messages(db: Session):
    return db.query(ScheduledMessage).order_by(ScheduledMessage.scheduled_time).all()
