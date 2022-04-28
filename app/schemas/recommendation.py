from typing import Dict, Optional

from pydantic import BaseModel


class RecommendationBase(BaseModel):
    pass


class Recommendation(RecommendationBase):   
    resume_id: int
    filename: str
    scores: Dict[str, float]
    final_score: float


class RecommendationRequest(RecommendationBase):
    tag_id: int
    job_id: int
    weights: Optional[Dict[str, float]] = 'default'
    n_scores: int


class RecommendationResponse(RecommendationRequest):
    recommendations: list[Recommendation]



