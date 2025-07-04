import json
from dapr.clients import DaprClient

from api.models import ScheduledMessage
from common.settings import Settings
from common.time import ensure_utc_aware

settings = Settings()

def publish_message_scheduled(message: ScheduledMessage):
    with DaprClient() as client:
        scheduled_utc = ensure_utc_aware(message.scheduled_time)
        client.publish_event(
            pubsub_name=settings.DAPR_PUBSUB_NAME,
            topic_name=settings.DAPR_TOPIC_NAME,
            data=json.dumps({
                'message_id': message.id,
                'content': message.content,
                'scheduled_time': scheduled_utc.isoformat()
            }),
            data_content_type='application/json',
        )
