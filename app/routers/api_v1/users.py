from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.crud import users as crud_users
from app.db.dependency import get_db
from app.routers.api_v1.config import Config

router = APIRouter(
    prefix=Config.PREFIX + '/users',
    tags=[Config.TAG, 'users'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.get('.get_all', response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_users.get_users(db, skip=skip, limit=limit)
    return users

@router.get('.get_by_id', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_users.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(404, 'User not found')
    return user

@router.post('.create', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_users.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='email already in use')
   
    new_user = crud_users.create_user(db, user)
    return new_user
