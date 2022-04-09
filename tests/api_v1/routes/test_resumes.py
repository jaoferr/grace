import os
import pathlib

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models import User
from tests.api_v1.conftest import TestClient, api_v1_config

PREFIX = api_v1_config.PREFIX + '/resumes'

def test_resume_ingest(client: TestClient, current_user: User):
    test_filename = 'resumes.zip'
    test_data_path = str(pathlib.Path(__file__).parent.joinpath('test_data', test_filename))
    
    data = {
        'tag': 'test_tag'
    }
    
    files = {
        'file': (test_filename, open(test_data_path, 'rb'), 'application/zip')
    }

    response = client.post(
        url=PREFIX + '/ingest', data=data, files=files
    )
    response_json = response.json()

    assert response.status_code == 202
    assert response_json.get('detail') == 'task was added to queue'
    assert len(response_json.get('batch_id')) == 24

def test_resume_ingest_invalid_file_type(client: TestClient, current_user: User):
    test_filename = 'resumes.zip'
    test_data_path = str(pathlib.Path(__file__).parent.joinpath('test_data', test_filename))
    
    data = {
        'tag': 'test_tag'
    }
    
    files = {
        'file': (test_filename, open(test_data_path, 'rb'), 'application/txt')
    }

    response = client.post(
        url=PREFIX + '/ingest', data=data, files=files
    )
    response_json = response.json()

    assert response.status_code == 400
    assert response_json.get('detail') == 'invalid file type'

def test_resume_tika_status(client: TestClient, current_user: User, tika_status_false: bool):
    test_filename = 'resumes.zip'
    test_data_path = str(pathlib.Path(__file__).parent.joinpath('test_data', test_filename))
    
    data = {
        'tag': 'test_tag'
    }
    
    files = {
        'file': (test_filename, open(test_data_path, 'rb'), 'application/txt')
    }

    response = client.post(
        url=PREFIX + '/ingest', data=data, files=files
    )
    response_json = response.json()

    assert response.status_code == 503
    assert response_json.get('detail') == 'ingest endpoint is not available'
