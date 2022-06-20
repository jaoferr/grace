import pathlib

import pytest
from fastapi.encoders import jsonable_encoder

from app.models import User
from app.crud import resumes as crud_resumes
from app.crud import tags as crud_tags
from app.schemas import resume as resume_schema
from app.schemas import tag as tag_schema
from tests.api_v1.conftest import AsyncClient, api_v1_config

PREFIX = api_v1_config.PREFIX + '/resumes'

@pytest.mark.asyncio
async def test_resume_ingest(client: AsyncClient, current_user: User):
    test_filename = 'resumes.zip'
    test_data_path = str(pathlib.Path(__file__).parent.joinpath('test_data', test_filename))
    
    data = {
        'tag_name': 'test_tag'
    }

    files = {
        'file': (test_filename, open(test_data_path, 'rb'), 'application/zip')
    }

    response = await client.post(
        url=PREFIX + '.ingest', data=data, files=files
    )
    response_json = response.json()

    assert response.status_code == 202
    assert response_json.get('detail') == 'task was added to queue'
    assert len(response_json.get('batch_id')) == 24

@pytest.mark.asyncio
async def test_resume_ingest_invalid_file_type(client: AsyncClient, current_user: User):
    test_filename = 'resumes.zip'
    test_data_path = str(pathlib.Path(__file__).parent.joinpath('test_data', test_filename))
    
    data = {
        'tag_name': 'test_tag'
    }

    files = {
        'file': (test_filename, open(test_data_path, 'rb'), 'application/txt')
    }

    response = await client.post(
        url=PREFIX + '.ingest', data=data, files=files
    )
    response_json = response.json()

    assert response.status_code == 400
    assert response_json.get('detail') == 'invalid file type'

@pytest.mark.asyncio
async def test_resume_tika_status(client: AsyncClient, current_user: User, tika_status_false: bool):
    test_filename = 'resumes.zip'
    test_data_path = str(pathlib.Path(__file__).parent.joinpath('test_data', test_filename))
    
    data = {
        'tag_name': 'test_tag'
    }

    files = {
        'file': (test_filename, open(test_data_path, 'rb'), 'application/txt')
    }

    response = await client.post(
        url=PREFIX + '.ingest', data=data, files=files
    )
    response_json = response.json()

    assert response.status_code == 503
    assert response_json.get('detail') == 'ingest endpoint is not available'

@pytest.mark.asyncio
async def test_update_resume(client: AsyncClient, current_user: User):
    tag = tag_schema.TagCreate(user_id=current_user.id, name='this is a test tag')
    db_tag = await crud_tags.create_tag(tag)
    resume = resume_schema.ResumeCreate(
        id=1, object_id='fakeobjectidfortestingx', 
        user_id=current_user.id, filename='filename.pdf',
        batch_id='fakeobjectidfortestingx', tag_id=db_tag.id, 
        content={'content': 'this is a test resume'},
        file=b'testbytes'
    )
    db_resume = await crud_resumes.create_resume(resume)
    resume_updates = resume_schema.ResumeUpdate(id=db_resume.id, tag_id=db_tag.id, content={'content': 'new test content'})

    data = jsonable_encoder(resume_updates)
    response = await client.post(
        url=PREFIX + '.update', json=data
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get('content') == resume_updates.content
    assert response_json.get('id') == resume_updates.id
    assert response_json.get('tag_id') == resume_updates.tag_id

@pytest.mark.asyncio
async def test_update_resume_fail(client: AsyncClient, current_user: User, second_generic_user: User):
    tag = tag_schema.TagCreate(user_id=second_generic_user.id, name='this is a test tag')
    db_tag = await crud_tags.create_tag(tag)
    resume = resume_schema.ResumeCreate(
        object_id='fakeobjectidfortestingx', 
        user_id=second_generic_user.id, filename='filename.pdf',
        batch_id='fakeobjectidfortestingx', tag_id=db_tag.id, 
        content={'content': 'this is a test resume'},
        file=b'testbytes'
    )
    db_resume = await crud_resumes.create_resume(resume)
    resume_updates = resume_schema.ResumeUpdate(id=db_resume.id, tag_id=db_tag.id, content={'content': 'new test content'})
    
    data = jsonable_encoder(resume_updates)
    response = await client.post(
        url=PREFIX + '.update', json=data
    )
    response_json = response.json()
    assert response.status_code == 404
    assert response_json.get('detail') == 'resume does not exist'

@pytest.mark.asyncio
async def test_delete_resume(client: AsyncClient, current_user: User, second_generic_user: User):
    tag = tag_schema.TagCreate(user_id=current_user.id, name='this is a test tag')
    db_tag = await crud_tags.create_tag(tag)
    resume = resume_schema.ResumeCreate(
        object_id='fakeobjectidfortestingx', 
        user_id=current_user.id, filename='filename.pdf',
        batch_id='fakeobjectidfortestingx', tag_id=db_tag.id, 
        content={'content': 'this is a test resume'}
    )
    db_resume = await crud_resumes.create_resume(resume)
    

    response = await client.post(
        url=PREFIX + '.delete', params={'resume_id': db_resume.id}
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json.get('object_id') == 'fakeobjectidfortestingx'
    assert response_json.get('success') == True

@pytest.mark.asyncio
async def test_delete_resume_fail(client: AsyncClient, current_user: User, second_generic_user: User):
    tag = tag_schema.TagCreate(user_id=second_generic_user.id, name='this is a test tag')
    db_tag = await crud_tags.create_tag(tag)
    resume = resume_schema.ResumeCreate(
        object_id='fakeobjectidfortestingx', 
        user_id=second_generic_user.id, filename='filename.pdf',
        batch_id='fakeobjectidfortestingx', tag_id=db_tag.id, 
        content={'content': 'this is a test resume'},
        file=b'testbytes'
    )
    db_resume = await crud_resumes.create_resume(resume)
    

    response = await client.post(
        url=PREFIX + '.delete', params={'resume_id': db_resume.id}
    )
    response_json = response.json()
    assert response.status_code == 404
    assert response_json.get('detail') == 'resume does not exist'
