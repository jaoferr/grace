from fastapi import Request
from starlette.responses import JSONResponse


class GenericAppException(Exception):
    
    def __init__(self, status_code: int, context: dict):
        self.exception = self.__class__.__name__
        self.status_code = status_code
        self.context = context
        
    def __str__(self) -> str:
        return f'<AppException {self.exception} - status_code={self.status_code} - context={self.context}>'

async def generic_app_exception_handler(request: Request, exc: GenericAppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'app_exception': exc.exception,
            'context': exc.context
        }
    )
    
class AppException:
    class DuplicateEntryException(GenericAppException):
        def __init__(self, context: dict = None):
            status_code = 409
            GenericAppException.__init__(status_code, context)
