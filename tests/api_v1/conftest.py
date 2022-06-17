from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient

from app.auth.token import get_current_user
from app.core.config import settings
from app.core.database import init_db, get_motor_client
from app.routers.api_v1.config import Config as api_v1_config
from app.crud import users as crud_users
from app.dependencies import get_tika_status
from app.models import User
from app.routers.api_v1 import auth, jobs, recommendation, resumes, users
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

    _app.include_router(users.router)
    _app.include_router(resumes.router)
    _app.include_router(auth.router)
    _app.include_router(jobs.router)
    _app.include_router(recommendation.router)

    return _app

@pytest.fixture(scope='function')
def app() -> Generator[FastAPI, Any, None]:
    _app = get_test_application()

    yield _app

@pytest.mark.asyncio
@pytest.fixture(scope='function')
async def client(app: FastAPI) -> Generator[AsyncClient, Any, None]:
    db_client = await get_motor_client()
    await init_db(db_client, database_name='testing')

    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        yield client
    
    db_client.drop_database('testing')
    

@pytest.fixture(scope='function')
def generic_user() -> Generator[User, Any, None]:
    user = schemas_users.UserCreate(
        username='generic_user', email='generic@email.com', password='generic_password'
    )
    db_user = crud_users.create_user(user)
    yield db_user

@pytest.fixture(scope='function')
def second_generic_user() -> Generator[User, Any, None]:
    user = schemas_users.UserCreate(
        username='generic_second_user', email='generic_second_user@email.com', password='generic_password'
    )
    db_user = crud_users.create_user(user)
    yield db_user

@pytest.fixture(scope='function')
def current_user(app: FastAPI, generic_user: User) -> Generator[User, Any, None]:
    def get_test_current_user():
        return generic_user

    app.dependency_overrides[get_current_user] = get_test_current_user
    return get_test_current_user()

@pytest.fixture(scope='function')
def tika_status_false(app: FastAPI):
    def fake_tika_status():
        return False

    app.dependency_overrides[get_tika_status] = fake_tika_status
