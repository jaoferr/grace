from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.auth.token import get_current_user
from app.core.config import settings
from app.crud import users as crud_users
from app.db.database import Base
from app.db.dependency import get_db
from app.dependencies import get_tika_status
from app.models import User
from app.routers.api_v1 import auth, jobs, main, recommendation, resumes, users
from app.routers.api_v1.config import Config as api_v1_config
from app.schemas import user as schemas_users

SQL_DATABASE_URI = 'sqlite://'
engine = create_engine(
    SQL_DATABASE_URI, connect_args={'check_same_thread': False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    _app.include_router(main.router)
    _app.include_router(resumes.router)
    _app.include_router(auth.router)
    _app.include_router(jobs.router)
    _app.include_router(recommendation.router)


    return _app

@pytest.fixture(scope='function')
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    _app = get_test_application()
    yield _app
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    def get_test_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope='function')
def generic_user(db_session: Session) -> Generator[User, Any, None]:
    user = schemas_users.UserCreate(
        username='generic_user', email='generic@email.com', password='generic_password'
    )
    db_user = crud_users.create_user(db_session, user)
    yield db_user

@pytest.fixture(scope='function')
def second_generic_user(db_session: Session) -> Generator[User, Any, None]:
    user = schemas_users.UserCreate(
        username='generic_second_user', email='generic_second_user@email.com', password='generic_password'
    )
    db_user = crud_users.create_user(db_session, user)
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
