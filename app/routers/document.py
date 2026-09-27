"""Document-related API endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.models.document import DocumentCreate, DocumentResponse
from app.services.document import (
    create_document,
    delete_document,
    get_document,
    get_documents,
)


# Create a router for document-related endpoints.
router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_document(document: DocumentCreate) -> DocumentResponse:
    """Create and store a new document."""

    return create_document(document)


@router.get(
    "",
    response_model=list[DocumentResponse],
)
def list_documents() -> list[DocumentResponse]:
    """Return all stored documents."""

    return get_documents()


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
)
def read_document(document_id: int) -> DocumentResponse:
    """Return a single document by its ID."""

    document = get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} was not found.",
        )

    return document


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_document(document_id: int) -> None:
    """Delete a document by its ID."""

    deleted = delete_document(document_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID {document_id} was not found.",
        )