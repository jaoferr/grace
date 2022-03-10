from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
from typing import Optional


def get_resume(db: Session, object_id: Optional[str] = None, id: Optional[int] = None):
    if object_id is not None:
        return db.query(models.ResumeIndex).filter(models.ResumeIndex.object_id == object_id).first()
    if id is not None:
        return db.query(models.ResumeIndex).filter(models.ResumeIndex.id == id).first()

def get_resumes_by_batch_id(db: Session, batch_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.ResumeIndex).filter(models.ResumeIndex.batch_id == batch_id).all()

def get_resumes_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.ResumeIndex) \
        .filter(models.ResumeIndex.user_id == user_id) \
        .offset(skip).limit(limit).all()

def create_resume(db: Session, resume: schemas.ResumeIndexCreate):  
    db_resume = models.ResumeIndex(**resume.dict())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ResumeIndex).offset(skip).limit(limit).all()
