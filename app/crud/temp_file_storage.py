from beanie.odm.fields import PydanticObjectId

from app.models.temp_file_storage import TempFileStorage


async def get_by_id(file_id: PydanticObjectId) -> TempFileStorage:
    return await TempFileStorage.get(file_id)

async def store(content: bytes) -> TempFileStorage:
    temp_file_in_db = TempFileStorage(file_content=content)
    return await temp_file_in_db.create()

async def remove(file_id: PydanticObjectId):
    return await TempFileStorage.get(file_id).delete()
    # return await TempFileStorage.find_one(TempFileStorage.id == file_id).delete()
