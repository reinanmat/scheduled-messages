import datetime

from dapr.actor import Actor, Remindable
from typing import Optional

from common.logger import logger
from scheduler.publish import publish_message
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
        message = data["message"]
        scheduled_time_iso = data["scheduled_time_iso"]

        if isinstance(scheduled_time_iso, str):
            scheduled_time = datetime.datetime.fromisoformat(scheduled_time_iso)
        elif isinstance(scheduled_time_iso, datetime.datetime):
            scheduled_time = scheduled_time_iso
        else:
            raise ValueError("scheduled_time_iso must be a string or datetime")

        logger.info(f"[SCHEDULER] Try scheduling message at {scheduled_time.isoformat()} - content: '{message}'")

        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            delay = max((scheduled_time - now), datetime.timedelta(seconds=0))

            await self.register_reminder(
                name="scheduled_pubsub_reminder",
                state=message.encode("utf-8"),
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
        message = state.decode("utf-8")
        logger.info(f"[REMINDER] Triggered '{name}' with message: '{message}'")

        publish_message(message)

        await self.unregister_reminder(name)
        logger.info(f"[REMINDER] Reminder '{name}' published and unregistered")
