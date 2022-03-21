from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc as sql_exc
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

engine, SessionLocal = start_sql_engine()
       

@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
