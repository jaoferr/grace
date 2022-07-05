from fastapi import (
    APIRouter, 
    Depends,
    HTTPException,
    UploadFile,
    Form
)
from beanie.odm.fields import PydanticObjectId

from app import schemas
from app.models import User
from app.services.auth import get_current_user
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

@router.post('.ingest', response_model=None)
async def ingest(
    file: UploadFile, 
    tag_id: PydanticObjectId = Form(...),
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends()
):
    current_user = handle_result(current_user)
    result = await resume_service.create_resumes(
        file=file.file,
        content_type=file.content_type,
        user_id=current_user.id
    )
    return handle_result(result)
