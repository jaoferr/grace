from typing import Generator, Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.dependency import get_db
from app.core.config import settings
from app.routers.api_v1 import users, main, resumes, auth, jobs, recommendation
from app.routers.api_v1.config import Config as api_v1_config

SQL_DATABASE_URI = 'sqlite:///./test_db.db'
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
