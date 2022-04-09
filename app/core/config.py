import os
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator
from sqlalchemy.engine.url import URL

basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    '''
    From fastapi docs:
    "Then, when you create an instance of that Settings class (in this case, in the settings object),
     Pydantic will read the environment variables in a case-insensitive way [...]"
    '''
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []   

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # sql db
    SQL_DRIVER: str
    SQL_ALEMBIC_DRIVER: str
    SQL_USER: str
    SQL_PASSWORD: str
    SQL_HOST: str
    SQL_PORT: str
    SQL_DATABASE: str    
    SQL_DATABASE_URI: Optional[str]

    # tika
    TIKA_ADAPTER: str
    TIKA_HOST: str
    TIKA_PORT: str


    class Config:
        case_sensitive = True
        env_file = ".env"
        basedir = basedir

    class Hardcoded:
        ALLOWED_EXTENSIONS = [
            'pdf', # 'doc', 'docx', 'jpeg', 'jpg'
        ]
        MAX_ZIP_FILE_SIZE = 1000 * 1e6  # 1GB


settings = Settings()

class SQLSettings:
    
    CONNECTION_STRING = URL.create(
        drivername=settings.SQL_DRIVER,
        username=settings.SQL_USER,
        password=settings.SQL_PASSWORD,
        host=settings.SQL_HOST,
        port=settings.SQL_PORT,
        database=settings.SQL_DATABASE
    )

    ALEMBIC_CONNECTION_STRING = URL.create(
        drivername=settings.SQL_ALEMBIC_DRIVER,
        username=settings.SQL_USER,
        password=settings.SQL_PASSWORD,
        host=settings.SQL_HOST,
        port=settings.SQL_PORT,
        database=settings.SQL_DATABASE
    )
