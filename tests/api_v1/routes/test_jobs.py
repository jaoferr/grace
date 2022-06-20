from datetime import datetime

import pytest
from fastapi.encoders import jsonable_encoder
from beanie.odm.fields import PydanticObjectId

from app.crud import jobs as crud_jobs
from app.models import User, Job
from app.schemas import jobs as jobs_schema
from tests.api_v1.conftest import AsyncClient, api_v1_config

PREFIX = api_v1_config.PREFIX + '/jobs'

# @pytest.mark.asyncio
# async def test_create_job(client: AsyncClient, current_user: User):
#     ''' Generic job creation '''
#     job = jobs_schema.JobCreateExternal(name="test job name", description='test job description')
#     data = jsonable_encoder(job)
#     response = await client.post(
#         url=PREFIX + '.create', json=data
#     )
#     response_json = response.json()

#     assert response.status_code == 200
#     assert response_json.get('name') == job.name
#     assert response_json.get('description') == job.description
#     assert response_json.get('user_id') == str(current_user.id)
#     assert isinstance(PydanticObjectId(response_json.get('id')), PydanticObjectId)
#     assert isinstance(datetime.fromisoformat(response_json.get('timestamp_added')), datetime)

# @pytest.mark.asyncio
# async def test_create_job_fail(client: AsyncClient, current_user: User):
#     ''' Tries to create a duplicated job '''
#     job = jobs_schema.JobCreate(name="test job name", description='test job description', user_id=current_user.id)
#     db_job = await crud_jobs.create_job(job)

#     data = jsonable_encoder(job)
#     response = await client.post(
#         url=PREFIX + '.create', json=data
#     )
#     response_json = response.json()

#     jobs = await Job.find_many(Job.user_id == job.user_id).to_list()  # TEMP

#     assert response.status_code == 400
#     assert response_json.get('detail') == 'job already exists'
    
@pytest.mark.asyncio
async def test_get_job_fail(
    client: AsyncClient, current_user: User,
    second_generic_user: User
):
    ''' Creates a job and tries to retrieve using another user '''
    job = jobs_schema.JobCreate(name="test job name", description='test job description', user_id=second_generic_user.id)
    db_job = await crud_jobs.create_job(job)

    response = await client.get(
        url=PREFIX + '.get_by_id', params={'job_id': db_job.id}
    )
    response_json = response.json()
    
    assert response.status_code == 404
    assert response_json.get('detail') == 'job not found'

# @pytest.mark.asyncio
# async def test_get_current_user_jobs(client: AsyncClient, current_user: User):
#     for i in range(3):
#         job = jobs_schema.JobCreate(name=f"test job name-{i}", description=f'job-{i}', user_id=current_user.id)
#         db_job = await crud_jobs.create_job(job)
        
#     response = await client.get(
#         url=PREFIX + '.from_current_user'
#     )
#     response_json = response.json()
    
#     assert response.status_code == 200
#     assert len(response_json) == 3
