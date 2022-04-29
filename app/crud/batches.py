import os
import shutil

from sqlalchemy.orm import Session

from app import models, schemas


def create_batch(db: Session, batch: schemas.BatchCreate):
    db_batch = models.Batch(**batch.dict())
    db.add(db_batch)
    db.commit()
    db.refresh(db_batch)
    return db_batch

def create_batch_dir(batch_id: str):
    batch_dir = os.path.join('app/data/', batch_id)
    if not os.path.exists(batch_dir):
        os.makedirs(batch_dir)

    return batch_dir

def delete_batch_dir(batch_id: str):
    batch_dir = os.path.join('app/data/', batch_id)
    try:
        shutil.rmtree(batch_dir)
        return True
    except:
        return False
