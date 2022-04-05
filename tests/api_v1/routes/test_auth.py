from sqlalchemy.orm import Session

from app.schemas import user as user_schema
from app.crud import users as crud_users
from tests.api_v1.conftest import TestClient, api_v1_config


PREFIX = api_v1_config.PREFIX + '/auth'

def test_login(client: TestClient, db_session: Session):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    db_user = crud_users.create_user(db_session, user)

    data = {'username': db_user.username, 'password': 'testpassword'}
    response = client.post(
        url=PREFIX + '/login', data=data
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json.get('token_type') == 'bearer'
    assert len(response_json.get('access_token')) == 128


def test_login_incorrect_password(client: TestClient, db_session: Session):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    db_user = crud_users.create_user(db_session, user)

    data = {'username': db_user.username, 'password': 'wrongtestpassword'}
    response = client.post(
        url=PREFIX + '/login', data=data
    )
    response_json = response.json()

    assert response.status_code == 401
    assert response_json.get('access_token') is None

def test_get_me(client: TestClient, db_session: Session):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    db_user = crud_users.create_user(db_session, user)

    data = {'username': db_user.username, 'password': 'testpassword'}
    login_response = client.post(
        url=PREFIX + '/login', data=data
    ).json()
    
    headers = {
        'Authorization': f'{login_response.get("token_type")} {login_response.get("access_token")}'
    }
    me_response = client.get(
        url=PREFIX + '/me', headers=headers
    )
    me_response_json = me_response.json()

    assert me_response_json.get('username') == db_user.username
    assert me_response_json.get('email') == db_user.email
    assert me_response_json.get('id') == db_user.id
    assert me_response_json.get('resume_count') == db_user.resume_count
