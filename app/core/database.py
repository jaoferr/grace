import motor.motor_asyncio
from beanie import init_beanie

from app.core.config import settings
from app.models import user, job, resume, tag

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.assemble_mongodb_conn_string()
    )
    
    await init_beanie(
        database=client[settings.MONGODB_DATABASE],
        document_models=[
            user.User, job.Job, resume.Resume, tag.Tag
        ]
    )
