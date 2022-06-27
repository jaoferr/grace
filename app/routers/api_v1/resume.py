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
    # background_tasks: BackgroundTasks,
    file: UploadFile, 
    tag_id: PydanticObjectId = Form(...),
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends()
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
    result = await resume_service.process_file(
        file=file.file,
        content_type=file.content_type,
        user_id=current_user.id
    )
    raise HTTPException(501, 'Not implemented')
    return handle_result(result)
