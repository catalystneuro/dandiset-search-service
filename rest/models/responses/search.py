from pydantic import BaseModel, Field


class PostSearchResponse(BaseModel):
    text: str