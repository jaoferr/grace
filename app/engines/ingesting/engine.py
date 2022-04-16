import os
import re
import string
from io import BytesIO
from typing import Any, Generator

import nltk
from nltk.corpus import stopwords
from tika import parser
from unidecode import unidecode

from app.dependencies import TikaServer


def basic_clean_up(text: str) -> str:
    text = unidecode(text)
    text = text.lower() \
        .replace('\n', ' ') \
        .strip() \
        .translate(str.maketrans('', '', string.punctuation))
    clean_up_pattern = re.compile(r'\b{}\b'.format(r'\b|\b'.join(stopwords.words())))  # removes stopwords
    text = clean_up_pattern.sub('', text)

    return text


class IngestingEngine:

    TIKA_SERVER_ENDPOINT = TikaServer.ENDPOINT

    def __init__(self) -> None:
        # if not os.path.exists('./venv/nltk_data/stopwords'):
            # nltk.download('stopwords', download_dir='./venv/')
        nltk.download('stopwords')

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

def get_engine() -> Generator[IngestingEngine, Any, None]:
    yield IngestingEngine()
