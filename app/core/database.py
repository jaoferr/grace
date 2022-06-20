from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models import User, Job, Resume, Tag


def get_motor_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(
        settings.assemble_mongodb_conn_string()
    )
    return client

async def init_db(
    client: AsyncIOMotorClient,
    database_name: str = settings.NOSQL_DATABASE
):

    await init_beanie(
        database=client[database_name],
        document_models=[
            User, Job, Resume, Tag
        ]
    )

from app.crud import users, jobs, tags
from app.schemas import UserCreate, JobCreate, TagCreate
async def init_defaults():
    user_x = await users.get_by_username('x') or await users.create_user(UserCreate(username='x', email='x', password='x'))
    user_y = await users.get_by_username('y') or await users.create_user(UserCreate(username='y', email='y', password='y'))

    job_1 = await jobs.get_by_user_and_name('Job 1', user_x.id) \
        or await jobs.create_job(JobCreate(name='Job 1', user_id=user_x.id, description='Job 1 description'))
    job_2 = await jobs.get_by_user_and_name('Job 2', user_y.id) \
        or await jobs.create_job(JobCreate(name='Job 2', user_id=user_y.id, description='Job 2 description'))

    tag_1 = await tags.get_by_user_and_name('Tag 1', user_x.id) \
        or await tags.create_tag(TagCreate(name='Tag 1', user_id=user_x.id, description='Tag 1 description'))
    tag_2 = await tags.get_by_user_and_name('Tag 2', user_y.id) \
        or await tags.create_tag(TagCreate(name='Tag 2', user_id=user_y.id, description='Tag 2 description'))
