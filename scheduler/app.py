import json
from dapr.clients import DaprClient, StateItem
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI

from common.logger import logger
from common.settings import Settings
from common.time import serialize_scheduled_message
from scheduler.schemas import MessageReceiver
from scheduler.worker import process_messages


app = FastAPI()
dapr_app = DaprApp(app)
settings = Settings()

@dapr_app.subscribe(pubsub=settings.DAPR_PUBSUB_NAME, topic=settings.DAPR_TOPIC_NAME)
def messages_subscriber(event: MessageReceiver):
    logger.info(f'subscriber received : {event.data["message_id"]}')

    with DaprClient() as client:
        key = f"message:{event.data['message_id']}"
        value = serialize_scheduled_message(
            message_id=event.data["message_id"],
            content=event.data["content"],
            scheduled_time=event.data["scheduled_time"]
        )

        state = StateItem(key=key, value=json.dumps(value), metadata={"contentType": "application/json"})

        client.save_bulk_state(
            store_name=settings.DAPR_STATESTORE_NAME,
            states=[state],
        )

    return { 'success' : True }


@app.post("/cron")
async def cron_event():
    logger.info('Cron event calling')
    await process_messages()
    logger.info('Cron event finish')
    return {"status": "done"}
