import os
import aiofiles
from io import BytesIO

from app.core.config import settings

data_path = settings.Hardcoded.DATA_PATH

async def save_locally(file: BytesIO, file_extension: str):
    pass

