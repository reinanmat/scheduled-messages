from dapr.actor import ActorId, ActorProxy
from dapr.clients import DaprClient

from common.schemas import ScheduledMessageFull
from common.settings import Settings
from scheduler.scheduler_actor_interface import SchedulerActorInterface

settings = Settings()


async def schedule_message_via_actor(message: ScheduledMessageFull):
    actor_id = ActorId(str(message.id))
    proxy = ActorProxy.create("SchedulerActor", actor_id, SchedulerActorInterface)
    await proxy.invoke_method("ScheduleMessage", message.model_dump_json().encode("utf-8")) 

def publish_message(message: ScheduledMessageFull):
    with DaprClient() as client:
        client.publish_event(
            pubsub_name=settings.DAPR_PUBSUB_NAME,
            topic_name=settings.DAPR_TOPIC_NAME,
            data=message.model_dump_json().encode("utf-8"),
            data_content_type='application/json',
        )
