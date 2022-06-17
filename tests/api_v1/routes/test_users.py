import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.crud import users as crud_users
from app.schemas import user as user_schema
from tests.api_v1.conftest import TestClient, api_v1_config

PREFIX = api_v1_config.PREFIX + '/users'

# @pytest.mark.asyncio
# async def test_create_user(client: AsyncClient):
#     user = user_schema.UserCreate(
#         username='testuser', email='testuser@domain.com', password='testpassword'
#     )
#     data = jsonable_encoder(user)
#     response = await client.post(
#         url=PREFIX + '.create', json=data
#     )
#     assert response.status_code == 200
#     assert response.json()['email'] == user.email

# @pytest.mark.asyncio
# async def test_create_user_already_exists(client: AsyncClient):
#     user = user_schema.UserCreate(username='testuser', email='testuser@domain.com', password='testpassword')
#     db_user = await crud_users.create_user(user)
#     data = jsonable_encoder(user)
#     response = await client.post(
#         url=PREFIX + '.create', json=data
#     )
    
#     assert response.status_code == 400

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    db_user = await crud_users.create_user(user)

    response = await client.post(
        url=PREFIX + '.get_by_id', data={'user_id': db_user.id}
    )
    response_json = response.json()

    assert response.status_code == 200
    assert response_json.get('id') == db_user.id
    assert response_json.get('email') == db_user.email
    assert response_json.get('username') == db_user.username
    assert response_json.get('resume_count') == db_user.resume_count

# @pytest.mark.asyncio
# async def test_get_user_404(client: AsyncClient):
#     response = await client.post(
#         url=PREFIX + '.get_by_id', data={'user_id': '99'}
#     )

#     assert response.status_code == 404
