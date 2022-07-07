from fastapi import APIRouter, Depends, HTTPException

from app import models, schemas
from app.services.auth import handled_get_current_user
from app.routers.api_v1.config import Config
from app.utils.service_result import handle_result


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
    current_user: models.User = Depends(handled_get_current_user)
):
    # if not (job:= crud_jobs.get_job_by_id(db, recommendation_request.job_id, current_user.id)):
    #     raise HTTPException(404, f'job not found with job_id "{recommendation_request.job_id}"')
    # if not (resumes:= crud_resumes.get_resumes_by_tag_id(db, recommendation_request.tag_id, current_user.id)):
    #     raise HTTPException(404, f'no resumes found with tag id {recommendation_request.tag_id}"')
    # results = recommend.launch_task(
    #     job=job,
    #     resumes=resumes,
    #     weighted_methods=recommendation_request.weights,
    #     n_scores=recommendation_request.n_scores
    # )

    # return results
    return HTTPException(501, 'Not implemented')

@router.get('.get_scoring_methods')
def list_scoring_methods():
    # return recommend.list_scoring_methods()
    return HTTPException(501, 'Not implemented')
