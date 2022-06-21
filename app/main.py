import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers.api_v1 import auth, job, recommendation, resume, tag, user
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
    # _app.include_router(resumes.router)
    _app.include_router(auth.router)
    _app.include_router(job.router)
    # _app.include_router(recommendation.router)
    _app.include_router(tag.router)


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
from fastapi.responses import JSONResponse

from app.core.logging import logger


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logger.error(f'{request}: {exc_str}')
    response = {'status_code': 422, 'detail': exc_str, 'data': str(request.__dict__)}
    return JSONResponse(content=response, status_code=422)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
