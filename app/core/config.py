import os
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    '''
    From fastapi docs:
    "Then, when you create an instance of that Settings class (in this case, in the settings object),
     Pydantic will read the environment variables in a case-insensitive way [...]"
    '''
    PROJECT_NAME: str
    PROJECT_VERSION: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []   

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # tika
    TIKA_ADAPTER: str
    TIKA_HOST: str
    TIKA_PORT: str

    # mongodb
    MONGODB_DRIVER: str
    MONGODB_HOST: str
    MONGODB_PORT: str
    MONGODB_DATABASE: str
    MONGODB_USER: str
    MONGODB_PASSWORD: str


    class Config:
        case_sensitive = True
        env_file = ".env"
        basedir = basedir

    class Hardcoded:
        ALLOWED_EXTENSIONS = [
            'pdf', # 'doc', 'docx', 'jpeg', 'jpg'
        ]
        MAX_ZIP_FILE_SIZE = 1000 * 1e6  # 1GB

    @classmethod
    def assemble_mongodb_conn_string(cls):
        conn_string = f'{cls.MONGODB_DRIVER}://{cls.MONGODB_USER}:{cls.MONGODB_PASSWORD}@{cls.MONGODB_HOST}:{cls.MONGODB_PORT}'
        return conn_string


settings = Settings()

