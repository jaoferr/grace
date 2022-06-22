from typing import Any, Generator, AsyncGenerator

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient

from app.services.auth import AuthService
from app.core.config import settings
from app.core.database import init_db, get_motor_client
from app.routers.api_v1.config import Config as api_v1_config
from app.crud import user as crud_users
from app.models import User
from app.routers.api_v1 import auth, job, recommendation, resume, tag, user
from app.schemas import user as schemas_users


def get_test_application():
    _app = FastAPI(title=settings.PROJECT_NAME + '_test', version='0.0.0')

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
    _app.include_router(tag.router)
    _app.include_router(recommendation.router)

    return _app

@pytest.fixture(scope='function')
def app() -> Generator[FastAPI, Any, None]:
    _app = get_test_application()

    yield _app

@pytest.mark.asyncio
@pytest.fixture(scope='function')
async def client(app: FastAPI) -> AsyncGenerator[Any, AsyncClient]:
    db_client = get_motor_client()
    await init_db(db_client, database_name='testing')

    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        yield client    

    db_client.drop_database('testing')

@pytest.mark.asyncio
@pytest.fixture(scope='function')
async def generic_user() -> AsyncGenerator[User, None]:
    user = schemas_users.UserCreate(
        username='generic_user', email='generic@email.com', password='generic_password'
    )
    db_user = await crud_users.create_user(user)
    yield db_user

@pytest.mark.asyncio
@pytest.fixture(scope='function')
async def second_generic_user() -> AsyncGenerator[User, None]:
    user = schemas_users.UserCreate(
        username='generic_second_user', email='generic_second_user@email.com', password='generic_password'
    )
    db_user = await crud_users.create_user(user)
    yield db_user

@pytest.fixture(scope='function')
def current_user(app: FastAPI, generic_user: User) -> User:
    def get_test_current_user():
        return generic_user

    auth_service = AuthService()
    auth_service.get_current_user = get_test_current_user
    app.dependency_overrides['auth_service'] = auth_service
    return get_test_current_user()
