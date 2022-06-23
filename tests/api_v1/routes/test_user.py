import pytest
import pytest_asyncio
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from beanie.odm.fields import PydanticObjectId

from app.crud import user as crud_users
from app.schemas import user as user_schema
from tests.api_v1.conftest import api_v1_config

PREFIX = api_v1_config.PREFIX + '/users'

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    data = jsonable_encoder(user)
    response = await client.post(
        url=PREFIX + '.create', json=data
    )

    assert response.status_code == 200
    assert response.json()['email'] == user.email

@pytest.mark.asyncio
async def test_create_user_already_exists(client: AsyncClient):
    user = user_schema.UserCreate(username='testuser', email='testuser@domain.com', password='testpassword')
    db_user = await crud_users.create_user(user)
    data = jsonable_encoder(user)
    response = await client.post(
        url=PREFIX + '.create', json=data
    )
    response_json = response.json()
    
    assert response.status_code == 409
    assert response_json.get('detail') == 'email already in use'

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    db_user = await crud_users.create_user(user)

    response = await client.post(
        url=PREFIX + '.get_by_id', params={'user_id': str(db_user.id)}
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json.get('id') == str(db_user.id)
    assert response_json.get('email') == db_user.email
    assert response_json.get('username') == db_user.username

@pytest.mark.asyncio
async def test_get_user_404(client: AsyncClient):
    oid = PydanticObjectId()
    response = await client.post(
        url=PREFIX + '.get_by_id', params={'user_id': str(oid)}
    )
    response_json = response.json()

    assert response.status_code == 404
    assert response_json.get('detail') == 'user not found'
