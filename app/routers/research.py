"""Research-related API endpoints."""

from fastapi import APIRouter, Depends

from app.dependencies import get_request_id
from app.models.research import ResearchRequest, ResearchResponse
from app.services.research import process_research


# Create a router for research-related endpoints.
router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


@router.post("", response_model=ResearchResponse)
async def create_research(
    request: ResearchRequest,
    request_id: str = Depends(get_request_id),
) -> ResearchResponse:
    """Process a research request and return the result."""

    return await process_research(
        query=request.query,
        request_id=request_id,
    )