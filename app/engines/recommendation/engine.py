import os
import re
from collections import Counter
from typing import Callable

import Levenshtein
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

from app.schemas.recommendation import Recommendation


class RecommendingEngine:

    def __init__(self, weighted_methods: dict[str: float] or str) -> None:
        self.weighted_methods = self.init_methods(weighted_methods)

        if not os.path.exists('./venv/nltk_data/punkt'):
            nltk.download('punkt', download_dir='./venv/nltk_data/')

    class Methods:

        def make_register():
            '''
            Makes funcions/methods decorated with this available as
            RecommendingEngine.Methods.available_methods
            '''
            registry = {}
            def register(fn: Callable):
                registry[fn.__name__] = fn
                return fn
            register.all = registry
            return register

        available_methods = make_register()

        @classmethod
        @available_methods
        def simple_word_count(cls, job: str, resume: str) -> float:
            '''
            Generic, simple word count.
            Counts the number of occurrences of each term of [job] in [resume].
            '''
            job_desc_token = nltk.tokenize.word_tokenize(job)
            sorted_job_token = sorted(job_desc_token, key=len, reverse=True)
            pattern = re.compile(
                '(?:\b{}\b)'.format('|'.join(map(re.escape, sorted_job_token)))
            )

            matches = pattern.findall(resume)
            word_count = Counter(matches)
            score = 0
            for word, freq in word_count.items():  # limits to 5 per term
                if freq > 5:
                    word_count[word] = 5
                    score += 5
                score += freq
            
            max_score = len(job_desc_token) * 5  # max score is 5x each term
            score_norm = score/max_score
            return score_norm

        @classmethod
        @available_methods
        def levenshtein_ratio(cls, job: str, resume: str) -> float:
            '''
            Simple Levenshtein Ratio
            Measures the difference between [job] and [resume], using Levenshtein distance formula.
            '''
            return Levenshtein.ratio(job, resume)

        @classmethod
        @available_methods
        def cosine_similarity(cls, job: str, resume: str) -> float:
            '''
            Simple Cosine Similarity
            Calculates the similarity between [job] and [resume] using cosines and math magic.
            '''
            unvector = [job, resume]
            vectorizer = CountVectorizer().fit_transform(unvector)
            vectors = vectorizer.toarray()

            vec0 = vectors[0].reshape(1, -1)
            vec1 = vectors[1].reshape(1, -1)
            similarity = sklearn_cosine_similarity(vec0, vec1)[0][0]
            return similarity

        @staticmethod
        @available_methods
        def test_method():
            pass


    def init_methods(self, weighted_methods: dict[str: float] or str) -> dict[str: float]:
        if not isinstance(weighted_methods, dict):
            valid_methods = {
                'simple_word_count': 0.3,
                'levenshtein_ratio': 0.3,
                'cosine_similarity': 0.4
            }
        
        else:
            valid_methods = {
                method: weight for method, weight in weighted_methods.items() \
                    if callable(getattr(self.Methods, method, None))
            }

        return valid_methods

    def run_methods(self, job: str, resume: str) -> float:
        score = {}
        final_score = 0
        for method, weight in self.weighted_methods.items():
            method_score = getattr(self.Methods, method)(job, resume)
            score[method] =  method_score * weight
            final_score += method_score * weight
        return score, final_score

    @staticmethod
    def get_best_scores(scores: list[Recommendation], n_scores: int = 5):
        sorted_scores = sorted(scores, key=lambda x: x.final_score, reverse=True)
        return sorted_scores[:n_scores]
