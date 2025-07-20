import json
from dapr.clients import DaprClient

from common.settings import Settings

settings = Settings()

def publish_message(message: str):
    with DaprClient() as client:
        client.publish_event(
            pubsub_name=settings.DAPR_PUBSUB_NAME,
            topic_name=settings.DAPR_TOPIC_NAME,
            data=json.dumps({
                'content': message,
            }),
            data_content_type='application/json',
        )
