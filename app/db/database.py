import time

from sqlalchemy import create_engine
from sqlalchemy import exc as sql_exc
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from app.core.config import SQLSettings
from app.core.logging import logger


def start_sql_engine():
    try:
        engine = create_engine(SQLSettings.CONNECTION_STRING, pool_pre_ping=True)
        engine.connect()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return engine, SessionLocal
    except sql_exc.SQLAlchemyError as err:
        logger.warning(err)
        logger.warning(f'Database server is not running. App will not work properly.')
        return None, None

attempt_no = 0
engine, SessionLocal = False, False
engine, SessionLocal = start_sql_engine()
while not (engine and SessionLocal):
    attempt_no += 1
    logger.warning(f'Retrying in 3s (attempt number {attempt_no})')
    time.sleep(3)
    engine, SessionLocal = start_sql_engine()
       

@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
