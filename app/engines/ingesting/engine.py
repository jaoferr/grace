from typing import BinaryIO

from tika import parser

from app.engines.main import GenericEngine
from app.core.config import settings


class IngestingEngine(GenericEngine):

    def __init__(
        self,
        *,
        endpoint: str = None
    ) -> None:
        self.endpoint = endpoint or settings.assemble_tika_endpoint()

    def extract_content(self, file_bytes: BinaryIO) -> dict[str: str]:
        ''' Process "any" file with tika '''
        parsed_pdf = parser.from_buffer(file_bytes.read(), serverEndpoint=self.endpoint)
        data = parsed_pdf.get('content')
        result = {
            'content': data
        }
        return result

    def validate_file_extension(self, filename: str) -> bool:
        return '.' in filename and filename.split('.')[-1].lower() \
            in settings.Hardcoded.ALLOWED_EXTENSIONS
