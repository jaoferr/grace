from sqlalchemy.orm import Session

from app import models, schemas
from app.engines.recommendation.engine import RecommendingEngine


def list_scoring_methods(engine: RecommendingEngine = RecommendingEngine):
    return {'methods': list(engine.Methods.available_methods.all.keys())}

def task(
    engine: RecommendingEngine,
    job: models.Jobs,
    resumes: list[models.Resume],
    n_scores: int
) -> list[schemas.Recommendation]:
    recommendations = []
    for resume in resumes:
        scores, final_score = engine.run_methods(
            job.description, resume.content.get('content')
        )
        recommendations.append(
            schemas.Recommendation(
                filename=resume.filename, scores=scores,
                final_score=final_score
            )
        )

    return engine.get_best_scores(recommendations, n_scores)


def launch_task(
    weighted_methods: dict[str: float],
    job: models.Jobs,
    resumes: list[models.Resume],
    n_scores: int
) -> list[schemas.Recommendation]:
    return task(
        RecommendingEngine(weighted_methods),
        job,
        resumes,
        n_scores
    )
