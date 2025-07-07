import json
from dapr.clients import DaprClient
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI

from common.logger import logger
from common.settings import Settings
from scheduler.schemas import MessageReceiver
from scheduler.worker import process_messages


app = FastAPI()
dapr_app = DaprApp(app)
settings = Settings()

def add_key_to_index(client: DaprClient, key: str):
    index_key = "message_index"
    try:
        raw_index = client.get_state(store_name=settings.DAPR_STATESTORE_NAME, key=index_key).data
        if raw_index:
            index = json.loads(raw_index)
        else:
            index = []
    except Exception:
        index = []

    if key not in index:
        index.append(key)
        client.save_state(store_name=settings.DAPR_STATESTORE_NAME, key=index_key, value=json.dumps(index))

@dapr_app.subscribe(pubsub=settings.DAPR_PUBSUB_NAME, topic=settings.DAPR_TOPIC_NAME)
def messages_subscriber(event: MessageReceiver):
    print('subscribe received : %s' % event.data['message_id'], flush=True)

    with DaprClient() as client:
        key = f"message:{event.data['message_id']}"
        value = json.dumps(event.data)
        client.save_state(store_name=settings.DAPR_STATESTORE_NAME, key=key, value=value)

        add_key_to_index(client, key)

    return { 'success' : True }


@app.post("/cron")
async def cron_event():
    logger.info('Cron event calling')
    await process_messages()
    logger.info('Cron event finish')
    return {"status": "done"}
