from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.crud import create_scheduled_message, get_all_messages, get_message_by_id, send_scheduled_message
from app.database import get_session
from app.schemas import MessageCreate, MessageOut

router = APIRouter()


@router.post('/schedule', response_model=MessageOut)
def create_message(msg: MessageCreate, db: Session = Depends(get_session)):
    return create_scheduled_message(db, msg)


@router.get('/messages/{msg_id}', response_model=MessageOut)
def get_message(msg_id: int, db: Session = Depends(get_session)):
    msg = get_message_by_id(db, msg_id)
    if not msg:
        raise HTTPException(status_code=404, detail='Message not found')
    return msg


@router.get('/messages', response_model=List[MessageOut])
def get_messages(db: Session = Depends(get_session)):
    return get_all_messages(db)


@router.put('/message/{msg_id}/send')
def send_message(msg_id: int, db: Session = Depends(get_session)):
    msg = get_message_by_id(db, msg_id)
    if not msg:
        raise HTTPException(status_code=404, detail='Message not found')
    if msg.sent:
        raise HTTPException(status_code=400, detail='Message already sent')

    try:
        send_scheduled_message(db, msg)
    except:
        raise HTTPException(status_code=500, detail='Failed to send message')
    
    return JSONResponse(status_code=200, content={ "detail": "Message sent successfully" })

