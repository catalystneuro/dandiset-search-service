from fastapi import APIRouter

router = APIRouter(prefix='/health-check', tags=["Health"])


@router.get("")
async def health_check() -> dict:
    return {"status": "ok"}
