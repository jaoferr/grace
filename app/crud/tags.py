from typing import Union

from pymongo.errors import DuplicateKeyError
from beanie.odm.fields import PydanticObjectId

from app import schemas
from app.models import Tag


async def get_by_query(query: schemas.TagQuery) -> Tag:
    return await Tag.find_one(query)

async def get_owned_by_user(user_id: int, skip: int, limit: int) -> list[Tag]:
    return await Tag.find_many(Tag.user_id == user_id) \
        .skip(skip).limit(limit) \
        .to_list()

async def get_by_user_and_name(tag_name: str, user_id: PydanticObjectId) -> Tag:
    tag = await Tag.find_one(Tag.name == tag_name, Tag.user_id == user_id)
    return tag

async def create_tag(new_tag: schemas.TagCreate) -> Union[Tag, str]:
    tag_db = Tag(
        name=new_tag.name,
        description=new_tag.description,
        user_id=new_tag.user_id,
        resumes=[]
    )

    try:
        return await tag_db.create()
    except DuplicateKeyError:
        return 'tag already exists'
