import time
from io import BufferedRandom, BytesIO
from zipfile import ZipFile

from fastapi import Depends
from beanie.odm.fields import PydanticObjectId

from app.core.logging import logger
from app.crud import resume as crud_resume
from app.engines.ingesting.engine import IngestingEngine
from app.core.worker import celery, update_progress
from app.schemas import ResumeCreate


@celery.task(name='ingest', bind=True)
async def ingest(
    self,
    *,
    raw_file: BufferedRandom,
    user_id: PydanticObjectId, 
    tag_id: PydanticObjectId,
    engine: IngestingEngine = Depends()
):
    zip = ZipFile(raw_file)
    full_queue_len = len(zip.infolist())

    for iqueue, file in enumerate(zip.infolist()):
        if engine.validate_file_extension(file.filename):
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

