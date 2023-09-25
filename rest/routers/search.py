from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Generator, Union

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
async def get_fields_data(req: PostSearchRequest): # -> Union[PostSearchResponse, StreamingResponse]:
    try:
        if req.stream:
            generator = search_service.suggest_relevant_dandisets(
                user_input=req.text,
                collection_name="dandi_collection",
                model="gpt-3.5-turbo-16k", 
                method=req.method,
                stream=req.stream,
            )
            print()
            print(f"Streaming responses for method {req.method}")
            print()
            return StreamingResponse(
                content=generator,
                # media_type="text/plain",
                media_type="application/json",
            )
        else:
            response = search_service.suggest_relevant_dandisets(
                user_input=req.text,
                collection_name="dandi_collection",
                model="gpt-3.5-turbo-16k", 
                method=req.method,
                stream=req.stream,
            )
            # import time
            # time.sleep(1)
            # response = req.text + req.method
            return PostSearchResponse(text=response)
    except (BadRequestException, UnauthorizedException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)