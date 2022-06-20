from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.auth.token import get_current_user
from app.routers.api_v1.config import Config


router = APIRouter(
    prefix=Config.PREFIX + '/tags',
    tags=[Config.TAG, 'tags'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.post('.from_user/{user_id}', response_model=list[schemas.Tag])
def get_resumes_from_user(user_id: int, skip: int = 0, limit: int = 20):
    # tags = crud_tags.get_tags_by_user_id(db, user_id, skip=skip, limit=limit)
    # return tags
    raise HTTPException(501, 'Not implemented')

@router.post('.from_current_user', response_model=list[schemas.Tag])
def get_resumes_from_current_user(
    skip: int = 0, limit: int = 20,
    current_user: models.User = Depends(get_current_user),
):
    # resumes = crud_tags.get_tags_by_user_id(db=db, user_id=current_user.id, skip=skip, limit=limit)
    # return resumes
    raise HTTPException(501, 'Not implemented')

@router.post('.create', response_model=schemas.Tag)
async def create_resume_tag(
    form_data: schemas.TagCreateExternal, 
    current_user: models.User = Depends(get_current_user),
):
    # new_tag = schemas.ResumeTagCreate(
    #     user_id=current_user.id,
    #     name=form_data.name,
    #     description=form_data.description
    # )
    # if (tag_db := crud_tags.create_tag(db, new_tag)):
    #     return tag_db
    raise HTTPException(501, 'Not implemented')

@router.get('.tag/{tag}', response_model=schemas.Tag)
def get_resumes_by_tag(
    tag: str, skip: int = 0, limit: int = 100,
    current_user: models.User = Depends(get_current_user)
    ):
#     if not (tag := (crud_constraints.tag_exists_and_belongs_to_user(db, user_id=current_user.id, tag=tag))):
#         raise HTTPException(status_code=404, detail=f'tag "{tag}" does not exist')

#     tag.resumes = tag.resumes[skip:limit]
#     return tag
    raise HTTPException(501, 'Not implemented')

@router.post('.update', response_model=schemas.Resume)
def update_resume(
    resume: schemas.ResumeUpdate,
    current_user: models.User = Depends(get_current_user)
    ) -> None:
    # if not crud_constraints.resume_exists_and_belongs_to_user(db, resume.id, current_user.id):
    #     raise HTTPException(status_code=404, detail='resume does not exist')

    # if not crud_constraints.tag_id_exists_and_belongs_to_user(db, resume.tag_id, current_user.id):
    #     raise HTTPException(status_code=404, detail='tag does not exist')

    # db_resume = crud_resumes.update_resume(db, resume, current_user)
    # return db_resume
    raise HTTPException(501, 'Not implemented')

@router.post('.delete', response_model=schemas.ResumeDelete)
def delete_resume(
    resume_id: int,
    current_user: models.User = Depends(get_current_user),
) -> None:
#     if not (resume := (crud_constraints.resume_exists_and_belongs_to_user(db, resume_id, current_user.id))):
#         raise HTTPException(status_code=404, detail='resume does not exist')

#     if not crud_constraints.tag_id_exists_and_belongs_to_user(db, resume.tag_id, current_user.id):
#         raise HTTPException(status_code=404, detail='tag does not exist')

#     if not (removed := crud_resumes.delete_resume(db, resume)):
#         raise HTTPException(status_code=500)
#     return {'id': removed, 'success': True}
    raise HTTPException(501, 'Not implemented')

