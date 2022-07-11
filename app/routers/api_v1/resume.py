from fastapi import (
    APIRouter, 
    Depends,
    UploadFile,
    Form
)
from beanie.odm.fields import PydanticObjectId

from app.schemas import TaskOut
from app.models import User
from app.services.auth import handled_get_current_user
from app.services.resume import ResumeService
from app.routers.api_v1.config import Config
from app.utils.service_result import handle_result


router = APIRouter(
    prefix=Config.PREFIX + '/resumes',
    tags=[Config.TAG, 'resumes'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.post('.ingest', response_model=TaskOut, status_code=202)
async def ingest(
    file: UploadFile, 
    tag_id: PydanticObjectId = Form(...),
    current_user: User = Depends(handled_get_current_user),
    resume_service: ResumeService = Depends()
):
    result = await resume_service.create_resumes(
        file=file.file,
        content_type=file.content_type,
        user_id=current_user.id,
        tag_id=tag_id
    )
    return handle_result(result)
