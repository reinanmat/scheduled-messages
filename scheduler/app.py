from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI

from common.logger import logger
from common.settings import Settings
from scheduler.schemas import MessageReceiver


app = FastAPI()
dapr_app = DaprApp(app)
settings = Settings()

@dapr_app.subscribe(pubsub=settings.DAPR_PUBSUB_NAME, topic=settings.DAPR_TOPIC_NAME)
def messages_subscriber(event: MessageReceiver):
    logger.info(f'[SCHEDULER] Subscribe received : {event.data["message_id"]}')

    return { 'success' : True }
