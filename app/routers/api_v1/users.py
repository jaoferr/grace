from app.routers.api_v1.config import Config
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.crud import users as crud_users
from app import schemas
from app.db.dependency import get_db


router = APIRouter(
    prefix=Config.PREFIX + '/users',
    tags=[Config.TAG, 'users'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.get('/', response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_users.get_users(db, skip=skip, limit=limit)
    return users

@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_users.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='email already in use')
   
    new_user = crud_users.create_user(db, user)
    return new_user

@router.get('/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_users.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(404, 'User not found')
    return user
