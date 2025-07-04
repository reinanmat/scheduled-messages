import json
from dapr.clients import DaprClient
from datetime import datetime, timedelta, timezone
from common.logger import logger
from common.settings import Settings


settings = Settings()

async def process_messages():
    logger.info('[CRON] Processing started')

    now = datetime.now(timezone.utc)
    next_minute = now + timedelta(minutes=1)

    with DaprClient() as client:
        index_state = client.get_state(store_name=settings.DAPR_STATESTORE_NAME, key="message_index").data

        if not index_state:
            logger.info('[CRON] No messages indexed')
            return

        try:
            message_keys = json.loads(index_state)
        except Exception as e:
            logger.error(f'[CRON] Failed to decode index: {e}')
            return

        remaining_keys = []

        for key in message_keys:
            state = client.get_state(store_name=settings.DAPR_STATESTORE_NAME, key=key)
            if not state.data:
                continue

            try:
                data = json.loads(state.data.decode())
            except Exception as e:
                logger.warning(f'[CRON] Failed to decode message data for {key}: {e}')
                continue

            scheduled_str = data.get('scheduled_time')
            if not scheduled_str:
                logger.warning(f'[CRON] Message {key} missing scheduled_time')
                continue

            try:
                scheduled_time = datetime.fromisoformat(scheduled_str)
            except ValueError:
                logger.warning(f'[CRON] Invalid scheduled_time format in {key}: {scheduled_str}')
                continue

            if now <= scheduled_time <= next_minute:
                logger.info(f'[CRON] Sending scheduled message: "{data["content"]}" at {scheduled_time.isoformat()}')
                client.delete_state(store_name=settings.DAPR_STATESTORE_NAME, key=key)
            else:
                remaining_keys.append(key)

        client.save_state(store_name=settings.DAPR_STATESTORE_NAME, key='message_index', value=json.dumps(remaining_keys))

    logger.info('[CRON] Processing finished')
