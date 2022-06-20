import pytest

from app.models import User
from tests.api_v1.conftest import AsyncClient, api_v1_config

PREFIX = api_v1_config.PREFIX + '/resumes'

@pytest.mark.asyncio
async def test_resume_ingest(client: AsyncClient, current_user: User):
    assert 202 == 503

@pytest.mark.asyncio
async def test_resume_ingest_invalid_file_type(client: AsyncClient, current_user: User):
    assert 202 == 503

@pytest.mark.asyncio
async def test_resume_tika_status(client: AsyncClient, current_user: User, tika_status_false: bool):
    assert 202 == 503

@pytest.mark.asyncio
async def test_delete_resume(client: AsyncClient, current_user: User, second_generic_user: User):
    assert 202 == 503

@pytest.mark.asyncio
async def test_delete_resume_fail(client: AsyncClient, current_user: User, second_generic_user: User):
    assert 202 == 503
