from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import constraints


def get_job(db: Session, job: schemas.JobQuery):
    return db.query(models.Jobs).filter_by(**job.dict()).first()

def get_job_by_id(db: Session, job_id: int, user_id: int):
    if constraints.job_exists_and_belongs_to_user(db, job_id=job_id, user_id=user_id):
        return

    return db.query(models.Jobs).filter_by(id=job_id, user_id=user_id).first()

def get_user_jobs(db: Session, user_id = int):
    return db.query(models.Jobs).filter_by(user_id=user_id).all()

def create_job(db: Session, job: schemas.JobCreate):
    if constraints.job_exists_and_belongs_to_user(db, user_id=job.user_id, description=job.description):
        return

    db_job = models.Jobs(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
