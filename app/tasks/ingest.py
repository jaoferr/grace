from tempfile import _TemporaryFileWrapper
from io import BytesIO, BufferedRandom
from zipfile import ZipFile
from bson import ObjectId
from sqlalchemy.orm import Session
from app.core.config import settings
from app.engines.ingesting.engine import IngestingEngine
from app.schemas import ResumeCreate, ResumeTagCreate, BatchCreate
from app.models import models
from app.crud import resumes, tags, batches
from app.core.logging import logger

def is_file_allowed(filename: str):
    return '.' in filename and filename.split('.')[-1].lower() in settings.Hardcoded.ALLOWED_EXTENSIONS

def update_progress(task_id: ObjectId, progress: int):
    pass

def task(raw_file: BufferedRandom, user: models.User, batch_id: str, tag: str, db: Session):
    tag = tags.create_tag(
        db, ResumeTagCreate(user_id=user.id, tag=tag)
    )
    batch = batches.create_batch(
        db, BatchCreate(id=batch_id, user_id=user.id)
    )
    engine = IngestingEngine()
    zip = ZipFile(raw_file)
    for file in zip.namelist():
        if is_file_allowed(file):
            resume_object_id = str(ObjectId())
            zip_bytes = zip.read(file)
            content = engine.process_file(BytesIO(zip_bytes))

            resumes.create_resume(
                db,
                ResumeCreate(
                    user_id=user.id, filename=file,
                    batch_id=batch.id, content=content,
                    object_id=resume_object_id, tag_id=tag.id
                )
            )
    logger.info(f'Done processing batch {batch_id}')

def launch_task(file: _TemporaryFileWrapper, user: models.User, batch_id: str, tag: str, db: Session):
    ''' add to queue '''
    task(file, user, batch_id, tag, db)
    file.close()
