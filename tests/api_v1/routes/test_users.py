from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.schemas import user as user_schema
from app.crud import users as crud_users
from tests.api_v1.conftest import TestClient, api_v1_config


def test_create_user(client: TestClient):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    data = jsonable_encoder(user)
    response = client.post(url=api_v1_config.PREFIX + '/users/', json=data)
    assert response.status_code == 200
    assert response.json()['email'] == user.email

def test_create_user_already_exists(client: TestClient, db_session: Session):
    user = user_schema.UserCreate(username='testuser', email='testuser@domain.com', password='testpassword')
    db_user = crud_users.create_user(db_session, user)
    data = jsonable_encoder(user)
    response = client.post(url=api_v1_config.PREFIX + '/users/', json=data)
    
    assert response.status_code == 400

def test_get_user(client: TestClient, db_session: Session):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    db_user = crud_users.create_user(db_session, user)

    response = client.get(
        url=api_v1_config.PREFIX + '/users', params={'user_id': db_user.id}
    ).json()
    assert db_user.id == response.get('id')
    assert db_user.email == response.get('email')
    assert db_user.username == response.get('username')
    assert db_user.resume_count == response.get('resume_count')

def test_get_user_404(client: TestClient):
    response = client.get(
        url=api_v1_config.PREFIX + '/users', params={'user_id': '99'}
    )
    
    assert response.status_code == 404
