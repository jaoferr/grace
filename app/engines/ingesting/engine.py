from io import BytesIO
from typing import Any, Generator

from tika import parser

from app.engines.main import GenericEngine
from app.core.config import settings


class IngestingEngine(GenericEngine):

    def __init__(self) -> None:
        self.endpoint = settings.assemble_tika_endpoint()

    def process_file(self, file_bytes: BytesIO):
        ''' Process "any" file with tika '''
        parsed_pdf = parser.from_buffer(file_bytes.read(), serverEndpoint=self.endpoint)
        data = parsed_pdf.get('content')
        result = {
            'content': data
        }
        return result
