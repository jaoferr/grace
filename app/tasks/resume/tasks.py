import os
from io import BufferedRandom, BytesIO
from tempfile import _TemporaryFileWrapper
from zipfile import ZipFile
import time

from fastapi import Depends

from app.core.config import settings
from app.core.logging import logger
from app.crud import resume, tag
from app.engines.ingesting.engine import IngestingEngine
from app.models import User
from app.core.worker import celery


def is_file_allowed(filename: str):
    return '.' in filename and filename.split('.')[-1].lower() in settings.Hardcoded.ALLOWED_EXTENSIONS

@celery.task(name='ingest', bind=True)
def ingest(
    # raw_file: BufferedRandom, user: User, 
    # batch_id: str, tag_name: str,
    self,
    task_duration: int,
    engine: IngestingEngine = Depends()
):
    # zip = ZipFile(raw_file)
    # for file in zip.infolist():
    #     if is_file_allowed(file.filename):
    #         resume_object_id = str(ObjectId())
    #         zip_bytes = zip.read(file)
    #         content = engine.process_file(BytesIO(zip_bytes))
    #         file.filename = f'{resume_object_id}_' + os.path.basename(file.filename)
    #         filepath = os.path.join(batch_dir, file.filename)
            
    #         zip.extract(file, batch_dir)
            
    #         resume.create_resume(
    #             db,
    #             ResumeCreate(
    #                 user_id=user.id, filename=filepath,
    #                 batch_id=batch.id, content=content,
    #                 object_id=resume_object_id, tag_id=tag.id
    #             )
    #         )

    # logger.info(f'Done processing batch {batch_id}')
    
    logger.info(f'Start task with duration={task_duration}')
    for i in range(task_duration):
        progress = round((i + 1) / task_duration * 100, 2)
        print(f'Progress: {progress}%')
        time.sleep(1)
        self.update_state(
            state='PROGRESS',
            meta={'progress': progress}
        )
    logger.info('Task finished')
