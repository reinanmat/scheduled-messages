from abc import abstractmethod

from dapr.actor import ActorInterface, actormethod


class SchedulerActorInterface(ActorInterface):
    @abstractmethod
    @actormethod(name='ScheduleMessage')
    async def schedule_message(self, data: dict) -> None:
        ...
