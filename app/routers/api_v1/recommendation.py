from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth.token import get_current_user
from app.crud import jobs as crud_jobs
from app.crud import resumes as crud_resumes
from app.db.dependency import get_db
from app.routers.api_v1.config import Config
from app.tasks import recommend

router = APIRouter(
    prefix=Config.PREFIX + '/recommend',
    tags=[Config.TAG, 'recommend'],
    responses={
        404: {'message': 'Not found'}
    }
)


@router.post('.make', response_model=list[schemas.Recommendation])
def make_recommendation(
    recommendation_request: schemas.RecommendationRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not (job:= crud_jobs.get_job_by_id(db, recommendation_request.job_id, current_user.id)):
        raise HTTPException(404, f'job not found with job_id "{recommendation_request.job_id}"')
    if not (resumes:= crud_resumes.get_resumes_by_tag_id(db, recommendation_request.tag_id, current_user.id)):
        raise HTTPException(404, f'no resumes found with tag id {recommendation_request.tag_id}"')
    results = recommend.launch_task(
        job=job,
        resumes=resumes,
        weighted_methods=recommendation_request.weights,
        n_scores=recommendation_request.n_scores
    )

    return results

@router.get('.get_scoring_methods')
def list_scoring_methods():
    return recommend.list_scoring_methods()
