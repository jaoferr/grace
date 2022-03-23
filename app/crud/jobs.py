from sqlalchemy.orm import Session
from app import models, schemas
from app.crud import constraints


def get_job(db: Session, job: schemas.JobQuery):
    return db.query(models.Jobs).filter_by(**job.dict()).first()

def get_job_by_id(db: Session, job_id: int):
    return db.query(models.Jobs).filter_by(id=job_id).first()

def get_user_jobs(db: Session, user_id = int):
    return db.query(models.Jobs).filter_by(user_id=user_id).all()

def create_job(db: Session, job: schemas.JobCreate):
    if constraints.job_exists_and_belongs_to_user(db, job.description, job.user_id):
        return get_job(db, job)

    db_job = models.Jobs(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
