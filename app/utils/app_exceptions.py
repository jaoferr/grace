from fastapi import Request
from starlette.responses import JSONResponse


class GenericAppException(Exception):
    
    def __init__(self, status_code: int, context: dict, is_public: bool):
        self.exception = self.__class__.__name__
        self.status_code = status_code
        self.context = context
        self.is_public = is_public
        
    def __str__(self) -> str:
        return f'<AppException {self.exception} - status_code={self.status_code} - context={self.context}>'

async def generic_app_exception_handler(request: Request, exc: GenericAppException) -> JSONResponse:
    if not exc.is_public:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'app_exception': exc.exception,
                'context': exc.context
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'detail': exc.context.get('detail')
        }
    )

class AppException:
    class DuplicateEntryException(GenericAppException):
        def __init__(self, context: dict = {}, is_public: bool = True):
            status_code = 409
            super().__init__(status_code, context, is_public)
    
    class EntryNotFound(GenericAppException):
        def __init__(self, context: dict = {}, is_public: bool = True):
            status_code = 404
            super().__init__(status_code, context, is_public)

    class Unauthorized(GenericAppException):
        def __init__(self, context: dict = {}, is_public: bool = True):
            status_code = 401
            context['detail'] = 'unauthorized'
            super().__init__(status_code, context, is_public)
            
    class InvalidCredentials(GenericAppException):
        def __init__(self, context: dict = {}, is_public: bool = True):
            status_code = 401
            context['detail'] = 'invalid credentials'
            super().__init__(status_code, context, is_public)

    class Disabled(GenericAppException):
        def __init__(self, context: dict = {}, is_public: bool = True):
            status_code = 400
            super().__init__(status_code, context, is_public)
