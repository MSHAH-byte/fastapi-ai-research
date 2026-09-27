"""Service logic for document-related operations."""

from datetime import datetime, timezone

from app.models.document import DocumentCreate, DocumentResponse


# In-memory storage used for learning purposes.
# Data will be lost whenever the application restarts.
_documents: dict[int, DocumentResponse] = {}

# Simple counter for generating document IDs.
_next_document_id = 1


def create_document(document: DocumentCreate) -> DocumentResponse:
    """Create and store a new document."""

    global _next_document_id

    new_document = DocumentResponse(
        id=_next_document_id,
        title=document.title,
        content=document.content,
        created_at=datetime.now(timezone.utc),
    )

    _documents[_next_document_id] = new_document
    _next_document_id += 1

    return new_document


def get_documents() -> list[DocumentResponse]:
    """Return all stored documents."""

    return list(_documents.values())


def get_document(document_id: int) -> DocumentResponse | None:
    """Return a document by ID, or None if it does not exist."""

    return _documents.get(document_id)


def delete_document(document_id: int) -> bool:
    """Delete a document by ID.

    Returns True if the document existed and was deleted.
    Returns False if the document did not exist.
    """

    if document_id not in _documents:
        return False

    del _documents[document_id]
    return True