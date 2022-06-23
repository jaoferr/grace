from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.core.logging import logger


async def generic_http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    logger.error(f'{request}: {exc.detail}')
    return JSONResponse(
        {'detail': exc.detail},
        status_code=exc.status_code
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={'detail': jsonable_encoder(exc.errors())}
    )
