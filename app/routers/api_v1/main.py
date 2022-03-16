from app.routers.api_v1.config import Config
from fastapi import APIRouter
from app.core.logging import logger


router = APIRouter(
    prefix=Config.PREFIX,
    tags=[Config.TAG, 'index'],
    responses={
        404: {'message': 'Not found'}
    }
)

msg = {'message': 'GRACE is running'}

@router.get('/')
async def index_msg():
    return msg
