from fastapi.encoders import jsonable_encoder

from app.schemas import user as user_schema
from tests.api_v1.conftest import TestClient, api_v1_config


def test_create_user(client: TestClient):
    user = user_schema.UserCreate(
        username='testuser', email='testuser@domain.com', password='testpassword'
    )
    data = jsonable_encoder(user)
    response = client.post(api_v1_config.PREFIX + '/users/', user.dict())
    assert response.status_code == 200
    assert response.json()['email'] == user.email
