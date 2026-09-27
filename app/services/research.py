"""Service logic for research-related operations."""

import asyncio

from app.models.research import ResearchResponse


async def process_research(
    query: str,
    request_id: str,
) -> ResearchResponse:
    """Process a research query using simulated asynchronous work.

    This is intentionally a mock service. In a real application, this
    function could call an LLM, search engine, or RAG pipeline.
    """

    # Simulate an asynchronous operation such as an API call.
    await asyncio.sleep(1)

    return ResearchResponse(
        request_id=request_id,
        query=query,
        answer=f"Mock research result for: {query}",
        sources=[
            "Mock Source 1",
            "Mock Source 2",
        ],
    )