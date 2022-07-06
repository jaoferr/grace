from datetime import datetime

from beanie import Document


class TempFileStorage(Document):
    timestamp_added: datetime = datetime.utcnow()
    file_content: bytes

    class Settings:
        name = 'temp_file_storage'
