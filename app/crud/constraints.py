from sqlalchemy.orm import Session
from app import schemas, models


def is_user_in_db(db: Session, user_id: int):
    return bool(db.query(models.User).filter(models.User.id == user_id).first())

def tag_exists_and_belongs_to_user(db: Session, tag: str, user_id: int):
    return bool(db.query(models.ResumeTag).filter_by(tag=tag, user_id=user_id).first())

def batch_exists_and_belongs_to_user(db: Session, batch_id: str, user_id: int):
    return bool(db.query(models.Batch).filter_by(id=batch_id, user_id=user_id).first())
