"""Main FastAPI application for the AI Research & Knowledge API."""

from fastapi import FastAPI

from app.routers import document, health, research


# Create the FastAPI application.
app = FastAPI(
    title="AI Research & Knowledge API",
    description="A learning project for building APIs with FastAPI.",
    version="1.0.0",
)


# Register the application's API routers.
app.include_router(health.router)
app.include_router(research.router)
app.include_router(document.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Return basic information about the API."""

    return {
        "message": "Welcome to the AI Research & Knowledge API",
        "docs": "/docs",
    }