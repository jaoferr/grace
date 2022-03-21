from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers.api_v1 import users, main, resumes, auth


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, version='0.2.0')

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(users.router)
    _app.include_router(main.router)
    _app.include_router(resumes.router)
    _app.include_router(auth.router)


    return _app

# check dependencies
from app.dependencies import dependencies

app = get_application()

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
