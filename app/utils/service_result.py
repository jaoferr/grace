import inspect
from typing import Any

from app.utils.app_exceptions import GenericAppException
from app.core.logging import logger

class ServiceResult:
    
    def __init__(self, arg):
        if isinstance(arg, GenericAppException):
            self.success = False
            self.exception = arg.exception
            self.status_code = arg.status_code
        else:
            self.success = True
            self.exception = None
            self.status_code = None
        self.value = arg
    
    def __str__(self) -> str:
        if self.success:
            return '[Success]'
        return f'[Exception]: {self.exception}'
    
    def __repr__(self) -> str:
        if self.success:
            return '<ServiceResult Success>'
        return f'<ServiceResult AppException {self.exception}>'
    
    def __enter__(self) -> Any:
        return self.value
    
    def __exit__(self, *kwargs):
        pass

def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f'{info.filename}:{info.function}:{info.lineno}'

def handle_result(result: ServiceResult):
    if not result.success:
        with result as exception:
            logger.error(f'{exception} | caller={caller_info()}')
            raise exception

    with result as result:
        return result
