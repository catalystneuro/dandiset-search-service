from pydantic import BaseModel, Field
from enum import Enum


class SearchMethods(str, Enum):
    simple = "simple"
    keywords = "keywords"


class PostSearchRequest(BaseModel):
    text: str = Field(..., description="User input text")
    method: SearchMethods = Field(SearchMethods.simple, description="Search method to use")