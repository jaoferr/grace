from io import BytesIO
from zipfile import ZipFile

import pytest
from beanie.odm.fields import PydanticObjectId

from app.models import User, Tag
from tests.api_v1.conftest import AsyncClient, api_v1_config

PREFIX = api_v1_config.PREFIX + '/resumes'

@pytest.mark.asyncio
async def test_resume_ingest(
    client: AsyncClient, 
    current_user: User,
    generic_tag: Tag
):
    data = {'tag_id': str(generic_tag.id)}
    fake_zip = BytesIO()
    with ZipFile(fake_zip, 'a') as zip_file:
        for i in range(3):
            fake_filename = f'fake_resume{i}.txt'
            fake_bytes = BytesIO(f'fake resume number {i}'.encode('utf-8'))
            zip_file.writestr(fake_filename, fake_bytes.getvalue())

    files={'file': ('filename', fake_zip, 'application/zip')}

    response = await client.post(
        url=PREFIX + '.ingest', data=data, files=files
    )
    response_json = response.json()

    assert response.status_code == 202
    assert response_json.get('detail') == ''
    assert PydanticObjectId.is_valid((response_json.get('task_id')))

# @pytest.mark.asyncio
# async def test_resume_ingest_invalid_file_type(client: AsyncClient, current_user: User):
#     assert 202 == 503

# @pytest.mark.asyncio
# async def test_resume_tika_status(client: AsyncClient, current_user: User):
#     assert 202 == 503

# @pytest.mark.asyncio
# async def test_delete_resume(client: AsyncClient, current_user: User, second_generic_user: User):
#     assert 202 == 503

# @pytest.mark.asyncio
# async def test_delete_resume_fail(client: AsyncClient, current_user: User, second_generic_user: User):
#     assert 202 == 503
