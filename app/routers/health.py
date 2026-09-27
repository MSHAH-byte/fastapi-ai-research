"""Health check API endpoints."""

from fastapi import APIRouter


# Create a router for health-related endpoints.
router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check() -> dict[str, str]:
    """Check whether the API is running."""

    return {
        "status": "ok",
        "message": "AI Research & Knowledge API is running",
    }