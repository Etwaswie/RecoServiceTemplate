import random
import typing
from typing import List

from fastapi import APIRouter, FastAPI, Request, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from service.api.authorization import APIKeys
from service.api.exceptions import AuthorizationError, ModelNotFoundError, UserNotFoundError
from service.api.recommenders import top_popular, top_popular_without_viewed, weighted_random_recommendation
from service.log import app_logger


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()
api_key_header = APIKeyHeader(name="Authorization")


def token_response(token: str = Security(api_key_header)) -> str:
    if token == APIKeys:
        return token
    else:
        raise AuthorizationError()


@router.get(
    path="/",
    tags=["Root"],
)
async def read_root() -> str:
    return "Welcome!"


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


@typing.no_type_check
@router.get(path="/reco/{model_name}/{user_id}", tags=["Recommendations"], response_model=RecoResponse)
async def get_reco(
    request: Request, model_name: str, user_id: int, token: str = Security(token_response)
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")
    k_recs = 10
    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    if model_name == "random":
        reco = random.sample(range(16518), k_recs)
    elif model_name == "top_20_popular":
        reco = top_popular(k_recs)
    elif model_name == "top_weighted_duration_random":
        reco = weighted_random_recommendation(k_recs)
    elif model_name == "top_popular_without_viewed":
        reco = top_popular_without_viewed(user_id, k_recs)
    else:
        raise ModelNotFoundError(error_message=f"Model {model_name} not found")

    resp = RecoResponse(user_id=user_id, items=reco)
    return resp


def add_views(app: FastAPI) -> None:
    app.include_router(router)
