from pydantic import BaseModel, Field


class PostSearchRequest(BaseModel):
    text: str