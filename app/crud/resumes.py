from app.models import Resume, Tag
from app import schemas


async def get_by_id(oid: str) -> Resume:
    return await Resume.get(oid)

async def get_by_id_and_user(resume_id: str, user_id: str) -> Resume:
    return await Resume.find_one(Resume.id == resume_id & Resume.user_id == user_id)

async def get_owned_by_user(user_id: str, skip: int = 0, limit: int = 100) -> list[Resume]:
    return await Resume.find_many(Resume.user_id == user_id) \
        .skip(skip).limit(limit) \
        .to_list()

async def get_by_tag_id(tag_id: str, skip: int = 0, limit: int = 100) -> list[Resume]:
    return await Resume.find_many(Resume.tag_id == tag_id) \
        .skip(skip).limit(limit) \
        .to_list()

async def get_by_tag_id_and_user(tag_id: str, user_id: str, skip: int = 0, limit: int = 100) -> list[Resume]:
    return await Resume.find_many(Resume.tag_id == tag_id & Tag.user_id == user_id) \
        .skip(skip).limit(limit) \
        .to_list()

async def create_resume(new_resume: schemas.ResumeCreate) -> Resume:
    resume_db = Resume(
        filename=new_resume.filename,
        user_id=new_resume.user_id,
        tag_id=new_resume.tag_id,
        content=new_resume.content
    )
    
    return await resume_db.create()

async def delete_by_id(oid: str) -> str:
    resume = await get_by_id(oid)
    return await resume.delete()


async def delete_all() -> None:
    # resume_delete = await Resume.delete_all()
    # tag_delete = await Tag.delete_all()
    raise NotImplementedError

async def delete_all_resumes() -> bool:
    # if os.path.exists('app/data/'):
    #     for root, dirnames, files in os.walk('app/data/'):
    #         for file in files:
    #             os.remove(os.path.join(root, file))

    # db.query(models.Resume).delete()
    # db.query(models.ResumeTag).delete()
    # db.query(models.Batch).delete()
    # db.commit()
    # return True
    raise NotImplementedError

async def delete_resume(resume: Resume):
    # os.remove(resume.filename)
    # if os.path.exists(resume.filename):
    #     return False

    # db.delete(resume)
    # db.commit()
    # return resume.id
    raise NotImplementedError