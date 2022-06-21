from datetime import datetime

import pytest
from fastapi.encoders import jsonable_encoder
from beanie.odm.fields import PydanticObjectId

from app.crud import tag as crud_tags
from app.models import User, Tag
from app.schemas import tag as tags_schema
from tests.api_v1.conftest import AsyncClient, api_v1_config

PREFIX = api_v1_config.PREFIX + '/tags'

@pytest.mark.asyncio
async def test_create_tag(client: AsyncClient, current_user: User):
    ''' Generic job creation '''
    tag = tags_schema.TagCreateExternal(name="test job name", description='test job description')
    data = jsonable_encoder(tag)
    response = await client.post(
        url=PREFIX + '.create', json=data
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json.get('name') == tag.name
    assert response_json.get('description') == tag.description
    assert response_json.get('user_id') == str(current_user.id)
    assert isinstance(PydanticObjectId(response_json.get('id')), PydanticObjectId)
    assert isinstance(datetime.fromisoformat(response_json.get('timestamp_added')), datetime)

@pytest.mark.asyncio
async def test_create_job_fail(client: AsyncClient, current_user: User):
    ''' Tries to create a duplicated job '''
    tag = tags_schema.TagCreate(name="test job name", description='test job description', user_id=current_user.id)
    db_job = await crud_tags.create_tag(tag)

    data = jsonable_encoder(tag)
    response = await client.post(
        url=PREFIX + '.create', json=data
    )
    response_json = response.json()

    assert response.status_code == 409
    assert response_json.get('detail') == 'tag already exists'
    
@pytest.mark.asyncio
async def test_get_job_fail(
    client: AsyncClient, current_user: User,
    second_generic_user: User
):
    ''' Creates a job and tries to retrieve using another user '''
    tag = tags_schema.TagCreate(name="test job name", description='test job description', user_id=second_generic_user.id)
    db_tag = await crud_tags.create_tag(tag)

    response = await client.get(
        url=PREFIX + '.get_by_id', params={'tag_id': db_tag.id}
    )
    response_json = response.json()

    assert response.status_code == 404
    assert response_json.get('detail') == 'tag not found'

@pytest.mark.asyncio
async def test_get_current_user_jobs(client: AsyncClient, current_user: User):
    for i in range(3):
        tag = tags_schema.TagCreate(name=f"test tag name-{i}", description=f'tag-{i}', user_id=current_user.id)
        db_job = await crud_tags.create_tag(tag)

    response = await client.get(
        url=PREFIX + '.from_current_user'
    )
    response_json = response.json()
    
    assert response.status_code == 200
    assert len(response_json) == 3
