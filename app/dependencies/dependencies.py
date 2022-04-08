import requests
from app.core.config import settings
from app.core.logging import logger

class TikaServer:

    ENDPOINT = f'{settings.TIKA_ADAPTER}{settings.TIKA_HOST}:{settings.TIKA_PORT}'
    

    @classmethod
    def check_server(cls):
        try:
            r = requests.get(cls.ENDPOINT)
            logger.info(f'Using tika server at {cls.ENDPOINT}')
            return True
        except requests.exceptions.ConnectionError as e:
            logger.warn(e)
            logger.warn('Tika server is not running. Ingestion endpoints will not work.')
            return False
        except Exception as e:
            logger.warn('Unknown error. Ingestion endpoints will not work.')
            logger.warn(e)
            return False

def get_tika_status() -> bool:
    return TikaServer.check_server()
