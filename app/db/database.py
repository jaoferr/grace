from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from app.core.config import SQLConnection, create_sql_connection_object


sql_connection_object = create_sql_connection_object()
engine = create_engine(
    sql_connection_object.connection_string, pool_pre_ping=True,
    connect_args=sql_connection_object.connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
