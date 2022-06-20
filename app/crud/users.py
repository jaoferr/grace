from pymongo.errors import DuplicateKeyError

from app import schemas
from app.models import User
from app.auth.token import get_password_hash

async def get_by_id(user_id: str) -> User:
    return await User.get(user_id)

async def get_by_username(username: str) -> User:
    return await User.find_one(User.username == username)

async def get_by_email(email: str) -> User:
    return await User.find_one(User.email == email)

async def create_user(new_user: schemas.UserCreate):
    user_in_db = User(
        email=new_user.email,
        username=new_user.username,
        password=await get_password_hash(new_user.password)
    )

    try:
        return await user_in_db.create()

    except DuplicateKeyError:
        return 'email already in use'
