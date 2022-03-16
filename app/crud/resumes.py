from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas


def get_resume(db: Session, id: Optional[int] = None):
    return db.query(models.Resume).filter(models.Resume.id == id).first()

def get_resume_by_object_id(db: Session, object_id: Optional[int] = None):
    return db.query(models.Resume).filter(models.Resume.object_id == object_id).first()

def get_resumes_by_batch_id(db: Session, batch_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Resume) \
        .filter(models.Resume.batch_id == batch_id) \
        .offset(skip).limit(limit).all()

def get_resumes_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Resume) \
        .filter(models.Resume.user_id == user_id) \
        .offset(skip).limit(limit).all()

def create_resume(db: Session, resume: schemas.ResumeCreate):
    db_resume = models.Resume(**resume.dict())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).offset(skip).limit(limit).all()
