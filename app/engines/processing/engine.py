import re
import string

import nltk
from nltk.corpus import stopwords
from unidecode import unidecode

from app.engines.main import GenericEngine


class ProcessingEngine(GenericEngine):

    def __init__(self) -> None:
        nltk.download('stopwords')

    @staticmethod
    def decode_utf(text: str) -> str:
        return unidecode(text)
   
    @staticmethod
    def remove_punctuation(text: str) -> str:
        return text.lower() \
            .replace('\n', ' ') \
            .strip() \
            .translate(str.maketrans('', '', string.punctuation))

    @staticmethod
    def remove_stopwords(text: str) -> str:
        clean_up_pattern = re.compile(
            r'\b{}\b'.format(r'\b|\b'.join(stopwords.words()))
            )
        return clean_up_pattern.sub('', text)
   
    def basic_clean_up(self, text: str) -> str:
        text = self.decode_uft(text)
        text = self.remove_punctuation(text)
        text = self.remove_stopwords(text)

        return text
