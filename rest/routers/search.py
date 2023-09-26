from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import asyncio

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
async def get_fields_data(req: PostSearchRequest):
    try:
        if req.stream:
            async def generator() -> AsyncGenerator[str, None]:
                async for result in search_service.suggest_relevant_dandisets(
                        user_input=req.text,
                        collection_name="dandi_collection",
                        model="gpt-3.5-turbo-16k", 
                        method=req.method,
                        stream=req.stream,
                    ):
                    yield result
            return StreamingResponse(
                content=generator(),
                media_type="text/plain",
            )
        else:
            # response = search_service.suggest_relevant_dandisets(
            #     user_input=req.text,
            #     collection_name="dandi_collection",
            #     model="gpt-3.5-turbo-16k", 
            #     method=req.method,
            #     stream=req.stream,
            # )
            response = req.text + req.method
            await asyncio.sleep(5)
            return PostSearchResponse(text=response)
    except (BadRequestException, UnauthorizedException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)