from typing import BinaryIO

from app.core.config import settings


max_filesize = settings.Hardcoded.MAX_ZIP_FILE_SIZE
allowed_content_type = settings.Hardcoded.ALLOWED_CONTENT_TYPE
allowed_file_extensions = settings.Hardcoded.ALLOWED_EXTENSIONS
   
async def validate_content_type(content_type: str) -> bool:
    return content_type in allowed_content_type

async def validate_file_size(file: BinaryIO) -> bool:
    current_size = 0
    for chunk in file:
        current_size += len(chunk)
        if current_size > max_filesize:
            return False

    return True
