from sqlalchemy.orm import Session

from app import models, schemas
from app.crud import constraints


def create_batch(db: Session, batch: schemas.BatchCreate):
    db_batch = models.Batch(**batch.dict())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch
