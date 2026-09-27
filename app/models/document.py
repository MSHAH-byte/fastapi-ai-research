"""Pydantic models for document-related API operations."""

from datetime import datetime

from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    """Request body for creating a document."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="The title of the document.",
    )

    content: str = Field(
        ...,
        min_length=1,
        description="The text content of the document.",
    )


class DocumentResponse(BaseModel):
    """Response representation of a stored document."""

    id: int = Field(
        ...,
        description="Unique identifier of the document.",
    )

    title: str = Field(
        ...,
        description="The title of the document.",
    )

    content: str = Field(
        ...,
        description="The text content of the document.",
    )

    created_at: datetime = Field(
        ...,
        description="UTC timestamp when the document was created.",
    )