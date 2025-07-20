from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from common.logger import logger
from api.services import create_scheduled_message, get_all_messages, get_message_by_id, send_scheduled_message
from api.database import get_session
from api.schemas import MessageCreate, MessageOut

router = APIRouter()


@router.post('/schedule', response_model=MessageOut)
def create_message(msg: MessageCreate, db: Session = Depends(get_session)):
    logger.info(f'[API] Scheduling the "{msg.content}" message for the "{msg.scheduled_time}" time')
    return create_scheduled_message(db, msg)


@router.get('/messages/{msg_id}', response_model=MessageOut)
def get_message(msg_id: int, db: Session = Depends(get_session)):
    logger.info(f'[API] Fetching message with id={msg_id}')
    msg = get_message_by_id(db, msg_id)
    if not msg:
        logger.warning(f'[API] Message with id={msg_id} not found')
        raise HTTPException(status_code=404, detail='Message not found')
    return msg


@router.get('/messages', response_model=List[MessageOut])
def get_messages(db: Session = Depends(get_session)):
    logger.info(f'[API] Fetching all messages')
    return get_all_messages(db)


@router.put('/message/{msg_id}/send')
def send_message(msg_id: int, db: Session = Depends(get_session)):
    logger.info(f'[API] Attempting to send message with id={msg_id}')
    msg = get_message_by_id(db, msg_id)
    if not msg:
        logger.warning(f'[API] Message with id={msg_id} not found')
        raise HTTPException(status_code=404, detail='Message not found')
    if msg.sent:
        logger.warning(f'[API] Message with id={msg_id} has already been sent')
        raise HTTPException(status_code=400, detail='Message already sent')

    try:
        send_scheduled_message(db, msg)
        logger.info(f'[API] Message with id={msg_id} sent successfully')
    except Exception as e:
        logger.exception(f'[API] Failed to send message with id={msg_id}: {e}')
        raise HTTPException(status_code=500, detail='Failed to send message')
    
    return JSONResponse(status_code=200, content={ "detail": "Message sent successfully" })

