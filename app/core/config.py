import os
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, validator
from sqlalchemy.engine import url

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
    SQL_USER: str
    SQL_PASSWORD: str
    SQL_HOST: str
    SQL_PORT: str
    SQL_DATABASE: str    
    SQL_DATABASE_URI: Optional[str]

    class Config:
        case_sensitive = True
        env_file = ".env"
        basedir = basedir


settings = Settings()

class SQLConnection:
    def __init__(self, server_driver: str = None, connection_string: str = None, connect_args: dict = None) -> None:
        self.app_settings = settings

        self.server_driver = server_driver or 'sqlite:///'
        self.connection_string = connection_string or 'sqlite:///' + os.path.join(settings.Config.basedir, 'app.db')
        self.connect_args = connect_args or {'check_same_thread': False}

def create_sql_connection_object(silent: bool = False, settings: Settings = settings):
    try:
        sql_connection = SQLConnection(settings.SQL_DRIVER)
        sql_connection.connection_string = f'{settings.SQL_DRIVER}://{settings.SQL_USER}:{settings.SQL_PASSWORD}@{settings.SQL_HOST}:{settings.SQL_PORT}/{settings.SQL_DATABASE}'
        sql_connection.connect_args = {}
        return sql_connection
    except Exception as e:
        if not silent:
            print('Invalid SQL connection arguments. Defaulting to SQLite.')
            print('Raised exception:', e)
        return SQLConnection()
