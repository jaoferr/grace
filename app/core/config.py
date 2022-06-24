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
    NOSQL_DRIVER: str
    NOSQL_HOST: str
    NOSQL_PORT: str
    NOSQL_DATABASE: str
    NOSQL_USER: str
    NOSQL_PASSWORD: str


    class Config:
        case_sensitive = True
        env_file = ".env"
        basedir = basedir

    class Hardcoded:
        ALLOWED_EXTENSIONS = [
            'pdf', # 'doc', 'docx', 'jpeg', 'jpg'
        ]
        MAX_ZIP_FILE_SIZE = 1000 * 1e6  # 1GB
        DATA_PATH = os.path.join('app', 'data')

    def assemble_mongodb_conn_string(self):
        conn_string = f'{self.NOSQL_DRIVER}://{self.NOSQL_USER}:{self.NOSQL_PASSWORD}@{self.NOSQL_HOST}:{self.NOSQL_PORT}'
        return conn_string

    def assemble_tika_endpoint(self):
        endpoint = f'{self.TIKA_ADAPTER}://{self.TIKA_HOST}:{self.TIKA_HOST}'
        return endpoint


settings = Settings()

