from typing import Union

from sqlalchemy.orm import Session

from app import models


def is_user_in_db(db: Session, user_id: int) -> Union[models.User, bool]:
    if user :=(db.query(models.User).filter(models.User.id == user_id).first()):
        return user
    return False

def tag_exists_and_belongs_to_user(db: Session, name: str, user_id: int) -> Union[models.ResumeTag, bool]:
    if tag := (db.query(models.ResumeTag).filter_by(name=name, user_id=user_id).first()):
        return tag
    return False

def tag_id_exists_and_belongs_to_user(db: Session, tag_id: int, user_id: int) -> Union[models.ResumeTag, bool]:
    if tag := (db.query(models.ResumeTag).filter_by(id=tag_id, user_id=user_id).first()):
        return tag
    return False

def batch_exists_and_belongs_to_user(db: Session, batch_id: str, user_id: int) -> Union[models.Batch, bool]:
    if batch := (db.query(models.Batch).filter_by(id=batch_id, user_id=user_id).first()):
        return batch
    return False

def job_exists_and_belongs_to_user(
    db: Session, user_id: int,
    name: str = None, description: str = None
) -> Union[models.Jobs, bool]:
    query_payload = {}
    if name:
        query_payload['name'] = name
    if description:
        query_payload['description'] = description

    if job := (db.query(models.Jobs).filter_by(user_id=user_id, **query_payload).first()):
        return job
    return False

def resume_exists_and_belongs_to_user(db: Session, resume_id: int, user_id: int) -> Union[models.Resume, bool]:
    if resume := (db.query(models.Resume).filter_by(id=resume_id, user_id=user_id).first()):
        return resume
    return False
