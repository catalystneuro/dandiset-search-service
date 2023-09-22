from pydantic import BaseModel


class BadRequestError(BaseModel):
    status_code: int = 400
    detail: str = "Bad request data"


class SomethingWrongError(BaseModel):
    status_code: int = 500
    detail: str = "Something went wrong"


class UnauthorizedError(BaseModel):
    status_code: int = 401
    detail: str = "Unauthorized"


class ForbiddenError(BaseModel):
    status_code: int = 403
    detail: str = "Forbidden"


class ConflictError(BaseModel):
    status_code: int = 409
    detail: str = "Conflict"


class ResourceNotFoundError(BaseModel):
    status_code: int = 404
    detail: str = "Resource not found"