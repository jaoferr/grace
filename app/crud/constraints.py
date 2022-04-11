from sqlalchemy.orm import Session

from app import models, schemas


def is_user_in_db(db: Session, user_id: int) -> bool:
    return bool(db.query(models.User).filter(models.User.id == user_id).first())

def tag_exists_and_belongs_to_user(db: Session, tag: str, user_id: int) -> bool:
    return bool(db.query(models.ResumeTag).filter_by(tag=tag, user_id=user_id).first())

def tag_id_exists_and_belongs_to_user(db: Session, tag_id: int, user_id: int) -> bool:
    return bool(db.query(models.ResumeTag).filter_by(id=tag_id, user_id=user_id).first())

def batch_exists_and_belongs_to_user(db: Session, batch_id: str, user_id: int) -> bool:
    return bool(db.query(models.Batch).filter_by(id=batch_id, user_id=user_id).first())

def job_exists_and_belongs_to_user(
    db: Session, user_id: int,
    description: str = None, job_id: int = None
) -> bool:
    if description:
        return bool(db.query(models.Jobs).filter_by(description=description, user_id=user_id).first())
    if job_id:
        return bool(db.query(models.Jobs).filter_by(id=job_id, user_id=user_id).first())

def resume_exists_and_belongs_to_user(db: Session, resume_id: int, user_id: int) -> bool:
    return bool(db.query(models.Resume).filter_by(id=resume_id, user_id=user_id).first())
