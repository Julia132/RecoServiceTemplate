from typing import List

from fastapi import APIRouter, FastAPI, Request
from pydantic import BaseModel

from service.api.exceptions import UserNotFoundError
from service.log import app_logger
from service.model.recsys_models import LightFM
from service.utils import verify_token


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    # Write your code here

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    if model_name == "rec_model_test":
        k_recs = request.app.state.k_recs
    elif model_name == "blending":
        blening = LightFM(path="blending", name_for_bot="blending")
        k_recs = blening.get_rec(user_id)

    return RecoResponse(user_id=user_id, items=list(range(k_recs)))


def add_views(app: FastAPI) -> None:
    app.include_router(router)
