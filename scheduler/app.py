import httpx
from contextlib import asynccontextmanager
from dapr.ext.fastapi import DaprActor, DaprApp
from fastapi import FastAPI
from dapr.actor.runtime.config import ActorRuntimeConfig, ActorTypeConfig, ActorReentrancyConfig
from dapr.actor.runtime.runtime import ActorRuntime
from pydantic import TypeAdapter

from common.logger import logger
from common.schemas import ScheduledMessageFull
from common.settings import Settings
from scheduler.scheduler_actor import SchedulerActor
from scheduler.schemas import MessageReceiver

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = ActorRuntimeConfig()
    config.update_actor_type_configs([
        ActorTypeConfig(
            actor_type=SchedulerActor.__name__,
            reentrancy=ActorReentrancyConfig(enabled=True),
        )
    ])
    ActorRuntime.set_actor_config(config)

    actor = DaprActor(app)
    await actor.register_actor(SchedulerActor)
    yield

app = FastAPI(title=f'{SchedulerActor.__name__}Service', lifespan=lifespan)

dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub=settings.DAPR_PUBSUB_NAME, topic=settings.DAPR_TOPIC_NAME)
async def messages_subscriber(event: MessageReceiver):
    try:
        message = TypeAdapter(ScheduledMessageFull).validate_python(event.data)
        logger.info(f"[SCHEDULER] Subscribe received - id: {message.id}, content: '{message.content}'")

        async with httpx.AsyncClient() as client:
            response = await client.put(f"http://localhost:8000/messages/{message.id}/send")
            response.raise_for_status()

        logger.info(f"[SCHEDULER] Message with id={message.id} processed successfully")
        return { 'success' : True }
    except Exception as e:
        logger.error(f"[SCHEDULER] Failed to process message: {e}")
        return { 'success' : False }
