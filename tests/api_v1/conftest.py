from typing import Any, Generator, AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from httpx import AsyncClient

from app.main import get_application
from app.services.auth import get_current_user
from app.core.config import settings
from app.core.database import init_db, get_motor_client
from app.routers.api_v1.config import Config as api_v1_config
from app.crud import user as crud_users
from app.models import User
from app.schemas import user as schemas_users
from app.utils.app_exceptions import GenericAppException, generic_app_exception_handler
from app.utils.request_exceptions import (
    generic_http_exception_handler,
    request_validation_exception_handler
)


@pytest.fixture(scope='function')
def app() -> Generator[FastAPI, Any, None]:
    test_app = get_application()
    test_app.__setattr__('title', settings.PROJECT_NAME + '_test')
    test_app.__setattr__('version', '0.0.0')


    @test_app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request: HTTPException, exc):
        return await generic_http_exception_handler(request, exc)

    @test_app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
        return await request_validation_exception_handler(request, exc)

    @test_app.exception_handler(GenericAppException)
    async def custom_app_exception_handler(request, e):
        return await generic_app_exception_handler(request, e)

    yield test_app

@pytest_asyncio.fixture(scope='function')
async def client(app: FastAPI) -> AsyncGenerator[Any, AsyncClient]:
    db_client = get_motor_client()
    await init_db(db_client, database_name='testing')

    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        yield client    

    db_client.drop_database('testing')

@pytest_asyncio.fixture(scope='function')
async def generic_user() -> AsyncGenerator[User, None]:
    user = schemas_users.UserCreate(
        username='generic_user', email='generic@email.com', password='generic_password'
    )
    db_user = await crud_users.create_user(user)
    yield db_user

@pytest_asyncio.fixture(scope='function')
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

    app.dependency_overrides[get_current_user] = get_test_current_user
    return get_test_current_user()
