from beanie.odm.fields import PydanticObjectId

from app.models.temp_file_storage import TempFileStorage


async def get_by_id(file_id: PydanticObjectId) -> TempFileStorage:
    temp_file_in_db = await TempFileStorage.get(file_id)
    return temp_file_in_db

async def store(content: bytes) -> TempFileStorage:
    temp_file_in_db = TempFileStorage(file_content=content)
    return await temp_file_in_db.create()

async def remove(file_id: PydanticObjectId):
    temp_file = await TempFileStorage.get(file_id)
    return await temp_file.delete()
