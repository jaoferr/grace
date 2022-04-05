from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.routers.api_v1.config import Config
from app.crud import jobs as crud_jobs
from app.db.dependency import get_db
from app.auth.token import get_current_user


router = APIRouter(
    prefix=Config.PREFIX + '/jobs',
    tags=[Config.TAG, 'jobs'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.get('/all', response_model=list[schemas.Job])
def get_all_jobs(db: Session = Depends(get_db)):
    return db.query(models.Jobs).all()

@router.get('/from_current_user', response_model=list[schemas.Job])
def get_jobs_from_current_user(
    skip: int = 0, limit: int = 20,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not (jobs := crud_jobs.get_user_jobs(db, current_user.id)):
        raise HTTPException(status_code=404, detail=f'user has no jobs')
    return jobs

@router.post('/create', response_model=schemas.Job)
def create_job(
    job: schemas.JobCreateExternal, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_job = crud_jobs.create_job(
        db, schemas.JobCreate(user_id=current_user.id, **job.dict())
    )
    if db_job is None:
        raise HTTPException(status_code=400, detail='job already exists')

    return db_job

@router.get('', response_model=schemas.Job)
def get_job_by_id(
    job_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not (job := crud_jobs.get_job_by_id(db, job_id, current_user.id)):
        raise HTTPException(status_code=404, detail=f'job not found')
    return job
