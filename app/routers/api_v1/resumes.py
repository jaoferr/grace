from app.routers.api_v1.config import Config
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.crud import resumes as crud_resumes
from app.schemas import schemas
from app.db.dependency import get_db
from bson.objectid import ObjectId
from app.crud import constraints


router = APIRouter(
    prefix=Config.PREFIX + '/resumes',
    tags=[Config.TAG, 'resumes'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.get('/{resume_id}', response_model=schemas.Resume)
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = crud_resumes.get_resume(db, id=resume_id)
    if resume is None:
        raise HTTPException(404, 'User not found')
    return resume

@router.get('/from_user/{user_id}', response_model=list[schemas.Resume])
def get_resumes_from_user(user_id: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    resumes = crud_resumes.get_resumes_user_id(db, user_id, skip=skip, limit=limit)
    return resumes

@router.get('/from_batch/{batch_id}', response_model=list[schemas.Resume])
def get_resumes_by_batch_id(batch_id: str, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    resumes = crud_resumes.get_resumes_by_batch_id(db, batch_id)
    return resumes

@router.post('/', response_model=schemas.Resume)
def create_resume(resume: schemas.ResumeIndexCreate, db: Session = Depends(get_db)):
    resume.object_id = ObjectId()
    db_resume = crud_resumes.get_resume(db, object_id=resume.object_id)
    if db_resume:
        raise HTTPException(status_code=400, detail='resume already exists in index')
    if not constraints.is_user_in_db(db, resume.user_id):
        raise HTTPException(status_code=404, detail='user not found')
    new_resume = crud_resumes.create_resume(db, resume)
    return new_resume

@router.get('/', response_model=list[schemas.Resume])
def get_all_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):  # debug
    resumes = crud_resumes.get_resumes(db, skip=skip, limit=limit)
    return resumes
