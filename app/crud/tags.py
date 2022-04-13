from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import constraints


def get_tag(db: Session, tag: schemas.ResumeTagQuery):
    return db.query(models.ResumeTag).filter_by(**tag.dict()).first()

def get_user_tags(db: Session, user_id = int):
    return db.query(models.ResumeTag).filter_by(user_id=user_id).all()

def create_tag(db: Session, tag: schemas.ResumeTagCreate) -> models.ResumeTag:
    if db_tag := (constraints.tag_exists_and_belongs_to_user(db, **tag.dict())):
        return db_tag

    db_tag = models.ResumeTag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
