from beanie.odm.fields import PydanticObjectId

from app import schemas
from app.models import User

async def get_by_id(user_id: PydanticObjectId) -> User:
    return await User.get(user_id)

async def get_by_username(username: str) -> User:
    return await User.find_one(User.username == username)

async def get_by_email(email: str) -> User:
    return await User.find_one(User.email == email)

async def create_user(new_user: schemas.UserCreate) -> User:
    user_in_db = User(**new_user.dict())
    return await user_in_db.create()
