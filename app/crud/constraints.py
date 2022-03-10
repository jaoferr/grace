from sqlalchemy.orm import Session
from app.models.models import User

def is_user_in_db(db: Session, user_id: int):
    return bool(db.query(User).filter(User.id == user_id).first())
