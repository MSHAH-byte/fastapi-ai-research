"""Reusable FastAPI dependencies for the AI Research & Knowledge API."""

from uuid import uuid4

from fastapi import Header


def get_request_id(x_request_id: str | None = Header(default=None)) -> str:
    """Return the incoming request ID or generate one if it is missing.

    Clients can optionally send an X-Request-ID header. If they don't,
    the API generates a unique ID for the request.
    """

    if x_request_id:
        return x_request_id

    return str(uuid4())