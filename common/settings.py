from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = 'postgresql://wuser:wpass@localhost:54321/scheduler-messages'
    DAPR_PUBSUB_NAME: str = 'redis-pubsub'
    DAPR_TOPIC_NAME: str = 'messagescheduled'

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
