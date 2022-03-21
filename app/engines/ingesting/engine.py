from tika import parser
from io import BytesIO
from unidecode import unidecode
from app.dependencies import TikaServer


class ResumeObject:

    def __init__(self, filename: str, content: str, content_id: str, batch_id: str):
        self.filename = filename
        self.content = content
        self.content_id = content_id  # hash from file content
        self.batch_id = batch_id

    def dict(self):
        return vars(self)


class IngestingEngine:

    TIKA_SERVER_ENDPOINT = TikaServer.ENDPOINT

    @classmethod
    def process_file(cls, file_bytes: BytesIO):
        ''' Process "any" file with tika '''
        parsed_pdf = parser.from_buffer(file_bytes.read(), serverEndpoint=cls.TIKA_SERVER_ENDPOINT)
        data = parsed_pdf.get('content')
        data = data.lower().replace('\n', '').strip()
        data = unidecode(data)
        # insert other processing steps here
        result = {
            'content': data
        }
        return result
