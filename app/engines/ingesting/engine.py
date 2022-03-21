from tika import parser
from io import BytesIO

from unidecode import unidecode
import string
import re
from nltk.corpus import stopwords

from app.dependencies import TikaServer


class ResumeObject:

    def __init__(self, filename: str, content: str, content_id: str, batch_id: str):
        self.filename = filename
        self.content = content
        self.content_id = content_id  # hash from file content
        self.batch_id = batch_id

    def dict(self):
        return vars(self)


def basic_clean_up(text: str) -> str:
    text = unidecode(text)
    text = text.lower() \
        .replace('\n', '') \
        .strip() \
        .translate(str.maketrans('', '', string.punctuation))
    clean_up_pattern = re.compile(r'\b{}\b'.format(r'\b|\b'.join(stopwords.words())))  # removes stopwords
    text = clean_up_pattern.sub('', text)

    return text


class IngestingEngine:

    TIKA_SERVER_ENDPOINT = TikaServer.ENDPOINT

    @classmethod
    def process_file(cls, file_bytes: BytesIO):
        ''' Process "any" file with tika '''
        parsed_pdf = parser.from_buffer(file_bytes.read(), serverEndpoint=cls.TIKA_SERVER_ENDPOINT)
        data = parsed_pdf.get('content')
        # insert other processing steps here
        data = basic_clean_up(data)
        result = {
            'content': data
        }
        return result