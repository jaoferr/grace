import asyncio
from io import BytesIO
from zipfile import ZipFile

from fastapi import Depends
from beanie.odm.fields import PydanticObjectId

from app.crud import resume as crud_resume
from io import BytesIO

from app.engines.ingesting.engine import IngestingEngine
from app.core.worker import celery, update_progress, celery_logger
from app.schemas import ResumeCreate
from app.crud import temp_file_storage as crud_temp_file_storage

@celery.task(name='ingest', bind=True)
def ingest(self, **kwargs):
    async def async_ingest(
        self,
        *,
        temp_file_id: PydanticObjectId,
        user_id: PydanticObjectId, 
        tag_id: PydanticObjectId,
        engine: IngestingEngine = Depends()
    ):
        
        raw_file_in_db = await crud_temp_file_storage.get_by_id(temp_file_id)
        raw_file_bytes = BytesIO(raw_file_in_db.file_content)
        zip = ZipFile(raw_file_bytes)
        full_queue_len = len(zip.infolist())

        for iqueue, file in enumerate(zip.infolist()):
            if engine.validate_file_extension(file.filename):
                celery_logger.info(f'Processing file {iqueue}/{full_queue_len}:{file.filename}')
                zip_bytes = zip.read(file)
                content = engine.extract_content(BytesIO(zip_bytes))

                new_resume = await crud_resume.create_resume(
                    ResumeCreate(
                        user_id=user_id, tag_id=tag_id,
                        file=zip_bytes, filename=file.filename,
                        content=content
                    )
                )

            update_progress(self, iqueue, full_queue_len)

        await crud_temp_file_storage.remove(temp_file_id)

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_ingest(self, **kwargs))
