from beanie.odm.fields import PydanticObjectId

from app.models import Job
from app import schemas


async def get_by_id(oid: PydanticObjectId):
    return await Job.get(oid)

async def get_by_id_and_user(id: PydanticObjectId, user_id: PydanticObjectId) -> Job:
    job = await Job.find_one(Job.id == id, Job.user_id == user_id)
    return job

async def get_by_user_and_name(name: str, user_id: PydanticObjectId) -> Job:
    job = await Job.find_one(Job.name == name, Job.user_id == user_id)
    return job
    
async def get_owned_by_user(user_id: PydanticObjectId, skip: int, limit: int) -> list[Job]:
    return await Job.find_many(Job.user_id == user_id) \
        .skip(skip).limit(limit) \
        .to_list()

async def create_job(new_job: schemas.JobCreate) -> Job:
    job_in_db = Job(**new_job.dict())
    return await job_in_db.create()
