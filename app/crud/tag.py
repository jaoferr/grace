from beanie.odm.fields import PydanticObjectId

from app import schemas
from app.models import Tag


async def get_by_id(id: PydanticObjectId) -> Tag:
    return await Tag.find_one(Tag.id == id)

async def get_by_id_and_user(id: PydanticObjectId, user_id: PydanticObjectId) -> Tag:
    tag = await Tag.find_one(Tag.id == id, Tag.user_id == user_id)
    return tag

async def get_by_query(query: schemas.TagQuery) -> Tag:
    return await Tag.find_one(query)

async def get_owned_by_user(user_id: PydanticObjectId, skip: int, limit: int) -> list[Tag]:
    return await Tag.find_many(Tag.user_id == user_id) \
        .skip(skip).limit(limit) \
        .to_list()

async def get_by_user_and_name(name: str, user_id: PydanticObjectId) -> Tag:
    tag = await Tag.find_one(Tag.name == name, Tag.user_id == user_id)
    return tag

async def create_tag(new_tag: schemas.TagCreate) -> Tag:
    tag_db = Tag(**new_tag.dict())
    return await tag_db.create()
