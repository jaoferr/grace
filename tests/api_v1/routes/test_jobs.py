from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import jobs as jobs_schema
from app.crud import jobs as crud_jobs
from tests.api_v1.conftest import TestClient, api_v1_config


PREFIX = api_v1_config.PREFIX + '/jobs'

def test_create_job(client: TestClient, current_user: User):
    ''' Generic job creation '''
    job = jobs_schema.JobCreateExternal(description='test job description')
    data = jsonable_encoder(job)
    response = client.post(
        url=PREFIX + '/create', json=data
    )
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json.get('description') == job.description
    assert response_json.get('user_id') == current_user.id
    assert response_json.get('id') == 1
    
def test_create_job_fail(client: TestClient, current_user: User, db_session: Session):
    ''' Tries to create a duplicated job '''
    job = jobs_schema.JobCreate(description='test job description', user_id=current_user.id)
    db_job = crud_jobs.create_job(db_session, job)

    data = jsonable_encoder(job)
    response = client.post(
        url=PREFIX + '/create', json=data
    )
    response_json = response.json()
    
    assert response.status_code == 400
    assert response_json.get('detail') == 'job already exists'
    
def test_get_job_fail(
    client: TestClient, current_user: User,
    second_generic_user: User, db_session: Session
):
    ''' Creates a job and tries to retrieve using another user '''
    job = jobs_schema.JobCreate(description='test job description', user_id=second_generic_user.id)
    db_job = crud_jobs.create_job(db_session, job)

    response = client.get(
        url=PREFIX, params={'job_id': db_job.id}
    )
    
    assert response.status_code == 404
    assert response.json().get('detail') == 'job not found'

def test_get_current_user_jobs(
    client: TestClient, current_user: User,
    db_session: Session
):
    for i in range(3):
        job = jobs_schema.JobCreate(description=f'job-{i}', user_id=current_user.id)
        db_job = crud_jobs.create_job(db_session, job)
        
    response = client.get(
        url=PREFIX + '/from_current_user'
    )
    response_json = response.json()
    
    assert response.status_code == 200
    assert len(response_json) == 3
