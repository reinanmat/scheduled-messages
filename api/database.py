from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from common.settings import Settings
from api.models import table_registry

settings = Settings()
engine = create_engine(settings.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session

table_registry.metadata.create_all(bind=engine)
