import pytest

from app.crud import users as crud_users
from app.schemas import user as user_schema
from tests.api_v1.conftest import AsyncClient, api_v1_config

PREFIX = api_v1_config.PREFIX + '/auth'

@pytest.mark.asyncio
async def test_login(client: AsyncClient):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    db_user = await crud_users.create_user(user)

    data = {'username': db_user.username, 'password': 'testpassword'}
    response = await client.post(
        url=PREFIX + '.login', data=data
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json.get('token_type') == 'bearer'
    assert len(response_json.get('access_token')) == 128

@pytest.mark.asyncio
async def test_login_incorrect_password(client: AsyncClient):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    db_user = await crud_users.create_user(user)

    data = {'username': db_user.username, 'password': 'wrongtestpassword'}
    response = await client.post(
        url=PREFIX + '.login', data=data
    )
    response_json = response.json()

    assert response.status_code == 401
    assert response_json.get('access_token') is None

@pytest.mark.asyncio
async def test_get_me(client: AsyncClient):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    db_user = await crud_users.create_user(user)

    data = {'username': db_user.username, 'password': 'testpassword'}
    login_response = await client.post(
        url=PREFIX + '.login', data=data
    )
    login_response_json = login_response.json()
    
    headers = {
        'Authorization': f'{login_response_json.get("token_type")} {login_response_json.get("access_token")}'
    }
    me_response = await client.get(
        url=PREFIX + '.me', headers=headers
    )
    me_response_json = me_response.json()

    assert me_response_json.get('username') == db_user.username
    assert me_response_json.get('email') == db_user.email
    assert me_response_json.get('id') == str(db_user.id)
