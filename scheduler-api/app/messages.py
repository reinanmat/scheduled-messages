from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import create_message, list_messages, get_message
from app.database import get_session
from app.schemas import MessageCreate, MessageOut

router = APIRouter()


@router.post('/schedule', response_model=MessageOut)
def schedule_message(msg: MessageCreate, db: Session = Depends(get_session)):
    return create_message(db, msg)


@router.get('/messages', response_model=List[MessageOut])
def get_messages(db: Session = Depends(get_session)):
    return list_messages(db)


@router.get('/messages/{msg_id}', response_model=MessageOut)
def get_message_by_id(msg_id: int, db: Session = Depends(get_session)):
    msg = get_message(db, msg_id)
    if not msg:
        raise HTTPException(status_code=404, detail='Message not found')
    return msg
