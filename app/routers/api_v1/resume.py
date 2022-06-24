import os

from fastapi import (
    APIRouter, 
    Depends,
    HTTPException,
    UploadFile,
    Form
)
from fastapi.responses import FileResponse
from beanie.odm.fields import PydanticObjectId

from app import schemas
from app.models import User
from app.services.auth import get_current_user
from app.crud import resume as crud_resumes
from app.routers.api_v1.config import Config


router = APIRouter(
    prefix=Config.PREFIX + '/resumes',
    tags=[Config.TAG, 'resumes'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.get('.from_current_user', response_model=None)
async def get_from_current_user(
    skip: int = 0, limit: int = 20,
    current_user: User = Depends(get_current_user),
):
    # return await crud_resumes.get_owned_by_user(user_id=current_user.id, skip=skip, limit=limit)
    return HTTPException(501, 'Not implemented')

@router.get('.get_by_id', response_model=None)
async def get_by_id(
    resume_id: int,
    current_user: User = Depends(get_current_user)
):
    # resume = await crud_resumes.get_by_id_and_user(resume_id, current_user.id)
    # if resume is None:
    #     raise HTTPException(404, 'Resume not found')
    # return resume
    return HTTPException(501, 'Not implemented')

@router.get('.get_file_by_id', response_model=None)
async def get_file_by_id(
    resume_id: int,
    current_user: User = Depends(get_current_user),
):
#     if not (resume := await crud_resumes.get_by_id_and_user(resume_id, current_user.id)):
#         raise HTTPException(404, 'Resume not found')

#     response = FileResponse(path=resume.filename, filename=os.path.basename(resume.filename))
    # return response
    raise HTTPException(501, 'Not implemented')

@router.post('.ingest', response_model=None)
async def ingest(
    # background_tasks: BackgroundTasks,
    file: UploadFile, 
    tag_id: PydanticObjectId = Form(...),
    # current_user: User = Depends(get_current_user),
    # engine: IngestingEngine = Depends(get_engine),
    # tika_status: bool = Depends(get_tika_status)
):
    # if not tika_status:
    #     raise HTTPException(503, detail='ingest endpoint is not available')

    # file_size: int = settings.Hardcoded.MAX_ZIP_FILE_SIZE
    # real_file_size = 0

    # if file.content_type not in ['application/x-zip-compressed', 'application/zip']:
    #     raise HTTPException(400, detail='invalid file type')

    # temp_file = NamedTemporaryFile(delete=False)
    # for chunk in file.file:
    #     real_file_size += len(chunk)
    #     if real_file_size > file_size:
    #         raise HTTPException(413, detail='file size exceeds limit')
    #     temp_file.write(chunk)

    # batch_id = str(ObjectId())
    # background_tasks.add_task(
    #     ingest.launch_task,
    #     file=temp_file, user=current_user,
    #     batch_id=batch_id, tag_name=tag_name,
    #     engine=engine
    # )
    # await file.close()

    # return {'detail': 'task was added to queue'}
    raise HTTPException(501, 'Not implemented')


@router.post('.by_tag_id', response_model=None)
async def get_by_tag_id(
    tag_id: PydanticObjectId, skip: int = 0, limit: int = 100,
    current_user: User = Depends(get_current_user)
    ):
    # if not (resumes := crud_resumes.get_by_tag_id_and_user(tag_id, current_user.id, skip, limit)):
    #     raise HTTPException(status_code=404, detail=f'tag does not exist')

    # return resumes[skip:limit]
    raise HTTPException(501, 'Not implemented')

@router.post('.update', response_model=None)
def update(
    # resume: schemas.ResumeUpdate,
    # current_user: User = Depends(get_current_user)
    ) -> None:
    # if not crud_constraints.resume_exists_and_belongs_to_user(db, resume.id, current_user.id):
    #     raise HTTPException(status_code=404, detail='resume does not exist')

    # if not crud_constraints.tag_id_exists_and_belongs_to_user(db, resume.tag_id, current_user.id):
    #     raise HTTPException(status_code=404, detail='tag does not exist')

    # db_resume = crud_resumes.update_resume(db, resume, current_user)
    # return db_resume
    raise HTTPException(501, 'Not implemented')

@router.post('.delete', response_model=None)
def delete(
    resume_id: int,
    current_user: User = Depends(get_current_user)
) -> None:
    # if not (resume := (crud_constraints.resume_exists_and_belongs_to_user(db, resume_id, current_user.id))):
    #     raise HTTPException(status_code=404, detail='resume does not exist')

    # if not crud_constraints.tag_id_exists_and_belongs_to_user(db, resume.tag_id, current_user.id):
    #     raise HTTPException(status_code=404, detail='tag does not exist')

    # if not (removed := crud_resumes.delete_resume(db, resume)):
    #     raise HTTPException(status_code=500)
    # return {'id': removed, 'success': True}
    raise HTTPException(501, 'Not implemented')
