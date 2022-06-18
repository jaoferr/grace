from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models import user, job, resume, tag


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
            user.User, job.Job, resume.Resume, tag.Tag
        ]
    )
