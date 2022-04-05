import os
import pathlib
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from tests.api_v1.conftest import TestClient, api_v1_config


PREFIX = api_v1_config.PREFIX + '/resumes'

def test_resume_ingest(client: TestClient):
    # test_data_path = str(pathlib.Path(__file__).parent.joinpath('test_data', 'resumes.zip'))
    # data = {
    #     'tag': 'test_tag',
    #     'file': open(test_data_path, 'rb')
    # }
    
    # response = client.post(
    #     url=PREFIX + '/ingest', data=data
    # )

    # assert response.status_code is not None
    pass