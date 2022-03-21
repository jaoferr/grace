from sqlalchemy.orm import Session
from app import models, schemas
from app.crud import constraints


def create_tag(db: Session, tag: schemas.ResumeTagCreate):
    if constraints.tag_exists_and_belongs_to_user(db, **tag.dict()):
        return schemas.ResumeTag(**tag.dict())

    db_tag = models.ResumeTag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag
