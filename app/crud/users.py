from sqlalchemy.orm import Session

from app import schemas
from app.models import models


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

from app.auth.token import get_password_hash

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        # **user.dict()
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
