import json
from dapr.clients import DaprClient
from datetime import datetime, timedelta, timezone
from common.logger import logger
from common.settings import Settings
from common.time import to_timestamp_ms


settings = Settings()

async def process_messages():
    logger.info('[CRON] Processing started')

    now = datetime.now(timezone.utc)
    next_minute = now + timedelta(minutes=1)

    with DaprClient() as client:
        query = {
            "filter": {
                "AND": [
                    {
                        "GTE": {
                            "value.scheduled_time": to_timestamp_ms(now)
                        }
                    },
                    {
                        "LTE": {
                            "value.scheduled_time": to_timestamp_ms(next_minute)
                        }
                    }
                ]
            }
        }

        try:
            response = client.query_state(store_name=settings.DAPR_STATESTORE_NAME, query=json.dumps(query))
            messages = response.results
        except Exception as e:
            logger.error(f'[CRON] Failed to query state: {e}')
            return

        if not messages:
            logger.info('[CRON] No messages to process')
            return

        for message in messages:
            key = message.key
            data = json.loads(message.value)

            logger.info(f'[CRON] Sending scheduled message: "{data["content"]}" at {data["scheduled_time_iso"]}')
            client.delete_state(store_name=settings.DAPR_STATESTORE_NAME, key=key)

    logger.info('[CRON] Processing finished')
