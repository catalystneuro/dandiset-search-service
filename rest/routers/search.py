from fastapi import APIRouter, Depends, HTTPException, status

from ..services.search import SearchService
from ..models.exceptions.base import BadRequestException, UnauthorizedException
from ..models.errors.base import UnauthorizedError, BadRequestError
from ..models.responses.search import PostSearchResponse
from ..models.requests.search import PostSearchRequest


router = APIRouter(prefix='/search', tags=["Search"])
search_service = SearchService()


@router.post(
    "",
    responses={
        status.HTTP_200_OK: {"model": PostSearchResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
        status.HTTP_400_BAD_REQUEST: {"model": BadRequestError},
    }
)
async def get_fields_data(req: PostSearchRequest) -> PostSearchResponse:
    try:
        # response = search_service.suggest_relevant_dandisets(user_input=req.text)
        response = {"text": "response text"}
        return response
    except (BadRequestException, UnauthorizedException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)