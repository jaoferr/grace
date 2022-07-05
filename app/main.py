import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.api_v1 import (
    auth,
    job,
    recommendation,
    resume,
    tag,
    user,
    task
)
from app.core.database import init_db, get_motor_client, init_defaults

def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(user.router)
    _app.include_router(resume.router)
    _app.include_router(auth.router)
    _app.include_router(job.router)
    # _app.include_router(recommendation.router)
    _app.include_router(tag.router)
    _app.include_router(task.router)  

    return _app

app = get_application()

@app.on_event('startup')
async def app_init():
    db_client = get_motor_client()
    await init_db(db_client)
    await init_defaults()

    if not os.path.exists(settings.Hardcoded.DATA_PATH):
        os.makedirs(settings.Hardcoded.DATA_PATH)

# temporary
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.utils.app_exceptions import GenericAppException, generic_app_exception_handler
from app.utils.request_exceptions import (
    generic_http_exception_handler,
    request_validation_exception_handler
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: HTTPException, exc):
    return await generic_http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    return await request_validation_exception_handler(request, exc)

@app.exception_handler(GenericAppException)
async def custom_app_exception_handler(request, e):
    return await generic_app_exception_handler(request, e)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
