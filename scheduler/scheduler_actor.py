import datetime

from dapr.actor import Actor, Remindable
from typing import Optional

from pydantic import TypeAdapter

from common.dapr_client import publish_message
from common.logger import logger
from common.schemas import ScheduledMessageFull
from scheduler.scheduler_actor_interface import SchedulerActorInterface


class SchedulerActor(Actor, SchedulerActorInterface, Remindable):
    def __init__(self, ctx, actor_id):
        super(SchedulerActor, self).__init__(ctx, actor_id)

    async def _on_activate(self) -> None:
        """An callback which will be called whenever actor is activated."""
        logger.info(f'Activate {self.__class__.__name__} actor!')

    async def _on_deactivate(self) -> None:
        """An callback which will be called whenever actor is deactivated."""
        logger.info(f'Deactivate {self.__class__.__name__} actor!')

    async def schedule_message(self, data: dict) -> None:
        message_obj = TypeAdapter(ScheduledMessageFull).validate_python(data)

        logger.info(f"[SCHEDULER] Try scheduling message at {message_obj.scheduled_time.isoformat()} - id: {message_obj.id} - content: '{message_obj.content}'")

        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            delay = max((message_obj.scheduled_time - now), datetime.timedelta(seconds=0))

            await self.register_reminder(
                name="scheduled_pubsub_reminder",
                state=message_obj.model_dump_json().encode("utf-8"),
                due_time=delay,
                period=datetime.timedelta(0),
            )
            logger.info("[SCHEDULER] Reminder successfully registered")
        except Exception as e:
            logger.error(f"[SCHEDULER] Failed to register reminder: {e}", exc_info=True)
            raise

    async def receive_reminder(
        self,
        name: str,
        state: bytes,
        due_time: datetime.timedelta,
        period: datetime.timedelta,
        ttl: Optional[datetime.timedelta] = None,
    ) -> None:
        """Callback triggered when a reminder is fired."""
        message_obj = TypeAdapter(ScheduledMessageFull).validate_json(state)
        logger.info(f"[REMINDER] Triggered {name} - id: {message_obj.id} - content: '{message_obj.content}'")

        publish_message(message_obj)

        await self.unregister_reminder(name)
        logger.info(f"[REMINDER] Reminder '{name}' published and unregistered")
