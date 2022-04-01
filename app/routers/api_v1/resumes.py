import csv
import os
from datetime import datetime
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, HTTPException, UploadFile, BackgroundTasks
from sqlalchemy.orm import Session
from bson.objectid import ObjectId
from app import models, schemas
from app.crud import resumes as crud_resumes
from app.crud import constraints as crud_constraints
from app.tasks import ingest
from app.dependencies import TikaServer
from app.core.config import settings
from app.db.dependency import get_db
from app.auth.token import get_current_user
from app.routers.api_v1.config import Config


router = APIRouter(
    prefix=Config.PREFIX + '/resumes',
    tags=[Config.TAG, 'resumes'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.get('/from_user/{user_id}', response_model=list[schemas.Resume])
def get_resumes_from_user(user_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    resumes = crud_resumes.get_resumes_by_user_id(db, user_id, skip=skip, limit=limit)
    return resumes

@router.get('/from_current_user/', response_model=list[schemas.Resume])
def get_resumes_from_current_user(skip: int = 0, limit: int = 20, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    resumes = crud_resumes.get_resumes_by_user_id(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return resumes

@router.get('/from_batch/{batch_id}', response_model=list[schemas.Resume])
def get_resumes_by_batch_id(
    batch_id: str, skip: int = 0, limit: int = 20, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    if not crud_constraints.batch_exists_and_belongs_to_user(db, user_id=current_user.id, batch_id=batch_id):
        raise HTTPException(status_code=404, detail=f'batch "{batch_id}" does not exist')
    
    resumes = crud_resumes.get_resumes_by_batch_id(db, skip=skip, limit=limit, batch_id=batch_id)
    return resumes

@router.get('/', response_model=list[schemas.Resume])
def get_all_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):  # debug
    resumes = crud_resumes.get_resumes(db, skip=skip, limit=limit)
    return resumes

@router.get('/content/{resume_id}', response_model=schemas.ResumeContent)
def get_resume_content(resume_id: int, db: Session = Depends(get_db)):  # to be removed
    resume = crud_resumes.get_resume(db, resume_id)
    if resume is None:
        raise HTTPException(status_code=404, detail='resume does not exist')
    if resume.content is None:
        return {'content_keys': []}

    content_keys = list(resume.content.keys())
    return {'content_keys': content_keys}

@router.post('/ingest', status_code=202)
async def ingest_resume(
    tag: str, 
    # tag: schemas.ResumeCreateExternal,
    file: UploadFile, background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    is_tika_running = TikaServer.check_server()
    if not is_tika_running:
        raise HTTPException(503, detail='ingest endpoint is not available')

    file_size: int = settings.Hardcoded.MAX_ZIP_FILE_SIZE
    real_file_size = 0

    if file.content_type not in ['application/x-zip-compressed', 'application/zip']:
        raise HTTPException(400, detail='invalid file type')

    temp_file = NamedTemporaryFile(delete=False)
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > file_size:
            raise HTTPException(413, detail='file size exceeds limit')
        temp_file.write(chunk)

    batch_id = str(ObjectId())
    background_tasks.add_task(
        ingest.launch_task, file=temp_file,
        user=current_user, batch_id=batch_id,
        db=db, tag=tag # .tag
    )
    await file.close()

    return {'detail': 'task was added to queue', 'batch_id': batch_id}

@router.get('/export/', status_code=202)
def export_resumes(current_user: models.User = Depends(get_current_user)):
    resumes: list[models.Resume] = current_user.resumes
    export_time = str(datetime.utcnow()).replace(" ", "_").replace(':', '-')
    filename = f'export_user_{current_user.username}_{export_time}.csv'
    filepath = os.path.join(settings.Config.basedir, 'export', filename)
    with open(filepath, 'w') as csvfile:
        outcsv = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ['user_id', 'object_id', 'filename', 'timestamp', 'id', 'batch_id', 'content']
        outcsv.writerow(header)
        for record in resumes:
            row = [
                record.user_id,
                record.object_id,
                record.filename,
                str(record.timestamp),
                record.id,
                record.batch_id,
                str(record.content).replace(',', ' ').replace(';', ' ').replace('\t', ' ')
            ]
            outcsv.writerow(row)

    return {'detail': f'exported user "{current_user.username}" resumes to {filepath}'}

@router.get('/{resume_id}', response_model=schemas.Resume)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = crud_resumes.get_resume(db, resume_id)
    if resume is None:
        raise HTTPException(404, 'User not found')
    return resume

@router.get('/tag/{tag}', response_model=schemas.ResumeTag)
def get_resumes_by_tag(
    tag: str, skip: int = 0, limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    if not crud_constraints.tag_exists_and_belongs_to_user(db, user_id=current_user.id, tag=tag):
        raise HTTPException(status_code=404, detail=f'tag "{tag}" does not exist')
    
    tag = db.query(models.ResumeTag).filter_by(tag=tag, user_id=current_user.id).first()
    tag.resumes = tag.resumes[skip:limit]

    return tag
