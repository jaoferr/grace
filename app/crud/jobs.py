from app.models import Job
from app import schemas


async def get_by_id(oid: str):
    return await Job.get(oid)

async def get_by_id_and_user(job_id: str, user_id: str):
    return await Job.find_one(Job.id == job_id & Job.user_id == user_id)

async def get_owned_by_user(user_id: str, skip: int = 0, limit: int = 20):
    return await Job.find_many(Job.user_id == user_id) \
        .skip(skip).limit(limit) \
        .to_list()

async def create_job(new_job: schemas.JobCreate):
    job_db = Job(
        name=new_job.name,
        description=new_job.description,
        user_id=new_job.user_id
    )

    return await job_db.create()
