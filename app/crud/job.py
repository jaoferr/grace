from typing import Union

from pymongo.errors import DuplicateKeyError
from beanie.odm.fields import PydanticObjectId

from app.models import Job
from app import schemas


async def get_by_id(oid: PydanticObjectId):
    return await Job.get(oid)

async def get_by_id_and_user(job_id: PydanticObjectId, user_id: PydanticObjectId) -> Job:
    job = await Job.find_one(Job.id == job_id, Job.user_id == user_id)
    return job

async def get_by_user_and_name(job_name: str, user_id: PydanticObjectId) -> Job:
    job = await Job.find_one(Job.name == job_name, Job.user_id == user_id)
    return job
    
async def get_owned_by_user(user_id: PydanticObjectId, skip: int = 0, limit: int = 20) -> list[Job]:
    return await Job.find_many(Job.user_id == user_id) \
        .skip(skip).limit(limit) \
        .to_list()

async def create_job(new_job: schemas.JobCreate) -> Union[Job, str]:
    job_db = Job(
        name=new_job.name,
        description=new_job.description,
        user_id=new_job.user_id
    )

    try: # to do: find a better way to do this
        return await job_db.create()
    except DuplicateKeyError:
        return 'job already exists'
