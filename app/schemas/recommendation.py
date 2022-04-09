from typing import Dict

from pydantic import BaseModel


class RecommendationBase(BaseModel):
    pass


class Recommendation(RecommendationBase):   
    filename: str
    scores: Dict[str, float]
    final_score: float


class RecommendationRequest(RecommendationBase):
    tag_id: int
    job_id: int
    weights: Dict[str, float]
    n_scores: int


class RecommendationResponse(RecommendationRequest):
    recommendations: list[Recommendation]



