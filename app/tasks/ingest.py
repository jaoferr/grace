import os
from io import BufferedRandom, BytesIO
from tempfile import _TemporaryFileWrapper
from zipfile import ZipFile

from bson import ObjectId
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import logger
from app.crud import batches, resumes, tags
from app.engines.ingesting.engine import IngestingEngine
from app.models import models
from app.schemas import BatchCreate, ResumeCreate, ResumeTagCreate


def is_file_allowed(filename: str):
    return '.' in filename and filename.split('.')[-1].lower() in settings.Hardcoded.ALLOWED_EXTENSIONS

def update_progress(task_id: ObjectId, progress: int):
    pass

def task(
    raw_file: BufferedRandom, user: models.User, 
    batch_id: str, tag_name: str, 
    engine: IngestingEngine, db: Session
):
    tag = tags.create_tag(
        db, ResumeTagCreate(
            user_id=user.id, 
            name=tag_name
        )
    )
    batch = batches.create_batch(
        db, BatchCreate(id=batch_id, user_id=user.id)
    )

    batch_dir = batches.create_batch_dir(batch.id)

    zip = ZipFile(raw_file)
    for file in zip.infolist():
        if is_file_allowed(file.filename):
            resume_object_id = str(ObjectId())
            zip_bytes = zip.read(file)
            content = engine.process_file(BytesIO(zip_bytes))
            file.filename = f'{resume_object_id}_' + os.path.basename(file.filename)
            filepath = os.path.join(batch_dir, file.filename)
            
            zip.extract(file, batch_dir)
            
            resumes.create_resume(
                db,
                ResumeCreate(
                    user_id=user.id, filename=filepath,
                    batch_id=batch.id, content=content,
                    object_id=resume_object_id, tag_id=tag.id
                )
            )
            

    logger.info(f'Done processing batch {batch_id}')

def launch_task(
    file: _TemporaryFileWrapper, user: models.User, 
    batch_id: str, tag_name: str, 
    engine: IngestingEngine, db: Session
):
    ''' add to queue '''
    task(file, user, batch_id, tag_name, engine, db)
    file.close()
