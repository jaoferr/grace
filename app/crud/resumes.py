import os
import shutil
from typing import Optional

from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import constraints


def get_resume(db: Session, id: Optional[int] = None, user_id: Optional[int] = None):
    if resume := constraints.resume_exists_and_belongs_to_user(db, id, user_id):
        return resume

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
    if not constraints.tag_id_exists_and_belongs_to_user(db, resume.tag_id, resume.user_id):
        return False

    db_resume = models.Resume(**resume.dict())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Resume).offset(skip).limit(limit).all()

def get_resumes_by_tag_id(db: Session, tag_id: int, user_id: int) -> Optional[list[models.Resume]]:
    if tag := (constraints.tag_id_exists_and_belongs_to_user(db, tag_id, user_id)):
        resumes = db.query(models.Resume).filter_by(user_id=user_id, tag_id=tag_id).all()
        return resumes

    return None

def delete_all_resumes(db: Session) -> bool:
    if os.path.exists('app/data/'):
        shutil.rmtree('app/data/')

    os.makedirs('app/data') 
    db.query(models.Resume).delete()
    db.commit()
    return True

def update_resume(db: Session, resume: schemas.ResumeUpdate, user: schemas.User) -> models.Resume:
    db_resume = db.query(models.Resume).filter_by(id=resume.id, user_id=user.id).first()

    for field, value in vars(resume).items():
        setattr(db_resume, field, value) if value else None

    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def delete_resume(db: Session, resume: models.Resume):
    os.remove(resume.filename)
    if os.path.exists(resume.filename):
        return False

    db.delete(resume)
    db.commit()
    return resume.id
