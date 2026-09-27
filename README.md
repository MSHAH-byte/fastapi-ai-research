# FastAPI AI Research & Knowledge API

A structured learning project built to develop a strong understanding of **FastAPI for AI Engineering backends**.

The project implements a small research and document-management API while deliberately keeping the application independent of external AI providers, databases, authentication systems, and frontend frameworks.

The purpose is not to build a production-ready research engine. Instead, the project focuses on understanding the **backend patterns and FastAPI concepts that will later be used in larger AI systems involving LLMs, RAG, agents, and AI automation**.

---

## Overview

Modern AI applications commonly need a backend API that sits between the client application and AI services.

A simplified architecture looks like:

```text
Flutter / Web / Other Client
            │
            ▼
       FastAPI Backend
            │
     ┌──────┴──────┐
     │             │
   Router       Dependencies
     │             │
     ▼             ▼
Request Models   Request ID
     │
     ▼
Service Layer
     │
 ┌───┴──────────────┐
 │                  │
Research Logic   Document Logic
 │                  │
 ▼                  ▼
Mock Processing  In-Memory Storage
 │                  │
 └────────┬─────────┘
          ▼
    Response Models
          │
          ▼
       Client
```

This project implements that structure using FastAPI.

---

# Learning Objectives

The main objectives of the project were to understand how to:

* Create and configure a FastAPI application
* Organize a FastAPI project into maintainable modules
* Separate API routing from application logic
* Define request bodies using Pydantic
* Validate incoming data automatically
* Define response schemas
* Work with path parameters
* Return appropriate HTTP status codes
* Handle application-level errors
* Use FastAPI's dependency injection system
* Read values from HTTP headers
* Generate request identifiers
* Build asynchronous endpoints
* Simulate asynchronous operations
* Maintain temporary in-memory application state
* Generate interactive API documentation automatically
* Understand the flow from HTTP request → router → service → response

---

# Features

## 1. Modular FastAPI Application

The application is divided into separate modules instead of placing every endpoint inside `main.py`.

The project separates:

* Application setup
* Routers
* Pydantic models
* Services
* Dependencies

This makes the code easier to understand and provides a structure that can scale when the application becomes larger.

---

## 2. API Routers

The application uses `APIRouter` to organize endpoints by responsibility.

Current routers:

* Health
* Research
* Documents

Each router has its own URL prefix and Swagger tag.

For example:

```python
router = APIRouter(
    prefix="/research",
    tags=["Research"],
)
```

The main application then registers the router:

```python
app.include_router(research.router)
```

This keeps `main.py` focused on application configuration rather than endpoint implementation.

---

# 3. Pydantic Request Models

Incoming JSON request bodies are represented using Pydantic models.

Example:

```python
class ResearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
    )
```

Instead of manually checking whether the client sent a valid query, FastAPI automatically validates the request using the model.

For example:

```json
{
  "query": "What is retrieval augmented generation?"
}
```

is valid.

While:

```json
{}
```

is rejected because `query` is required.

Similarly:

```json
{
  "query": ""
}
```

is rejected because the minimum length is one character.

---

# 4. Response Models

The API also explicitly defines the structure of its responses.

For example:

```python
class ResearchResponse(BaseModel):
    request_id: str
    query: str
    answer: str
    sources: list[str]
```

The endpoint declares:

```python
@router.post("", response_model=ResearchResponse)
```

This provides a clear contract for the API response and allows FastAPI to document the response schema automatically.

---

# 5. Dependency Injection

The research endpoint demonstrates FastAPI dependency injection.

The application defines a reusable dependency:

```python
def get_request_id(
    x_request_id: str | None = Header(default=None),
) -> str:
    if x_request_id:
        return x_request_id

    return str(uuid4())
```

The endpoint uses it with:

```python
request_id: str = Depends(get_request_id)
```

This means the endpoint does not need to manually handle the request ID.

FastAPI resolves the dependency before calling the endpoint.

### Without a request ID

If the client does not provide:

```text
X-Request-ID
```

the application generates a UUID.

### With a request ID

If the client sends:

```text
X-Request-ID: my-test-request-001
```

the same value is returned in the response.

This demonstrates how dependencies can provide reusable logic to multiple endpoints.

---

# 6. Asynchronous Processing

The research endpoint is asynchronous:

```python
async def create_research(...):
```

The service also performs asynchronous work:

```python
await asyncio.sleep(1)
```

The one-second delay is intentionally simulated.

It represents the type of operation that might happen in a real AI application, such as:

* Calling an LLM API
* Calling a search API
* Querying a RAG system
* Waiting for another asynchronous service

No external service is used in this project.

The purpose is to understand the structure of asynchronous FastAPI endpoints before introducing real AI services.

---

# 7. Service Layer

Business/application logic is kept outside the routers.

For research:

```text
app/routers/research.py
        │
        ▼
app/services/research.py
```

The router handles the HTTP side of the operation.

The service handles the processing.

This separation is useful because the same service logic can later be called from different interfaces or workflows without duplicating the implementation.

---

# 8. In-Memory Document Storage

The document service uses a Python dictionary as temporary storage:

```python
_documents: dict[int, DocumentResponse] = {}
```

Documents can be:

* Created
* Retrieved individually
* Listed
* Deleted

No database is used.

### Important limitation

Because the data exists only in Python memory:

```text
Application starts
       ↓
Empty storage
       ↓
Create documents
       ↓
Documents exist in memory
       ↓
Application restarts
       ↓
Documents are lost
```

This is intentional.

The project is focused on FastAPI concepts rather than database integration.

A production application could later replace this service with PostgreSQL, MongoDB, or another persistent database.

---

# API Endpoints

## Health Check

### `GET /health`

Checks whether the API is running.

Example response:

```json
{
  "status": "ok",
  "message": "AI Research & Knowledge API is running"
}
```

---

# Research API

## `POST /research`

Processes a research query using simulated asynchronous processing.

### Request

```json
{
  "query": "What is retrieval augmented generation?"
}
```

### Response

```json
{
  "request_id": "8f1eef3a-8bf5-4390-8b72-a30898dbc789",
  "query": "What is retrieval augmented generation?",
  "answer": "Mock research result for: What is retrieval augmented generation?",
  "sources": [
    "Mock Source 1",
    "Mock Source 2"
  ]
}
```

### Request ID Behavior

If no `X-Request-ID` header is supplied, the API generates a UUID.

If the client supplies:

```text
X-Request-ID: my-test-request-001
```

the response contains:

```json
{
  "request_id": "my-test-request-001"
}
```

---

# Document API

## `POST /documents`

Creates a new document.

### Request

```json
{
  "title": "FastAPI Notes",
  "content": "FastAPI is a Python framework for building APIs."
}
```

### Response

```json
{
  "id": 1,
  "title": "FastAPI Notes",
  "content": "FastAPI is a Python framework for building APIs.",
  "created_at": "2026-09-27T15:30:00Z"
}
```

The endpoint returns:

```text
201 Created
```

---

## `GET /documents`

Returns all documents currently stored in memory.

Example:

```json
[
  {
    "id": 1,
    "title": "FastAPI Notes",
    "content": "FastAPI is a Python framework for building APIs.",
    "created_at": "2026-09-27T15:30:00Z"
  }
]
```

---

## `GET /documents/{document_id}`

Returns one document using its ID.

Example:

```text
GET /documents/1
```

If document `1` exists, it is returned.

If it does not exist, the API raises a `404 Not Found` error.

Example:

```json
{
  "detail": "Document with ID 999 was not found."
}
```

---

## `DELETE /documents/{document_id}`

Deletes a document by ID.

Example:

```text
DELETE /documents/1
```

A successful deletion returns:

```text
204 No Content
```

If the document does not exist:

```text
404 Not Found
```

is returned.

---

# Validation and Error Handling

FastAPI automatically handles request validation through Pydantic.

For example, `ResearchRequest` requires:

```text
query
```

and limits it to:

```text
Minimum length: 1
Maximum length: 500
```

Invalid input results in FastAPI returning:

```text
422 Unprocessable Entity
```

Application-level errors are handled explicitly using `HTTPException`.

For example:

```python
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Document with ID {document_id} was not found.",
)
```

This creates a distinction between:

### 422 — Validation Error

The request does not satisfy the expected input schema.

### 404 — Not Found

The request is valid, but the requested resource does not exist.

### 201 — Created

A new document was successfully created.

### 204 — No Content

A document was successfully deleted and there is no response body.

---

# Project Structure

```text
fastapi-ai-research/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── research.py
│   │   └── document.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── research.py
│   │   └── document.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── research.py
│   │   └── document.py
│   │
│   └── dependencies.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

# Folder Responsibilities

## `app/main.py`

Creates the FastAPI application and registers the routers.

It is the application's entry point.

---

## `app/routers/`

Contains HTTP endpoints.

Routers are responsible for:

* HTTP methods
* URL paths
* Request parameters
* Request bodies
* Calling dependencies
* Calling services
* Returning responses

### `health.py`

Contains the health-check endpoint.

### `research.py`

Contains research-related endpoints.

### `document.py`

Contains document CRUD endpoints.

---

## `app/models/`

Contains Pydantic models.

Models define:

* Expected request data
* Validation rules
* Response structures
* API schemas

---

## `app/services/`

Contains application logic.

Services are responsible for:

* Processing research requests
* Managing documents
* Managing temporary in-memory state

---

## `app/dependencies.py`

Contains reusable FastAPI dependencies.

Currently it provides request ID handling.

---

# Installation

## Requirements

* Python 3.12+
* pip
* Windows, macOS, or Linux

---

## 1. Clone the repository

```bash
git clone https://github.com/MSHAH-byte/fastapi-ai-research.git
```

Then:

```bash
cd fastapi-ai-research
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

---

## 3. Activate the virtual environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the development server:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

# Interactive API Documentation

FastAPI automatically generates OpenAPI documentation.

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to:

* View all endpoints
* Inspect request schemas
* Inspect response schemas
* Enter request data
* Execute API requests
* View response status codes
* Inspect generated cURL commands

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

ReDoc provides another automatically generated interface for exploring the API.

---

# Example Request Flow

A research request demonstrates the complete application flow:

```text
POST /research
       │
       ▼
FastAPI Router
       │
       ▼
ResearchRequest validation
       │
       ▼
get_request_id dependency
       │
       ▼
create_research()
       │
       ▼
process_research()
       │
       ▼
Simulated async processing
       │
       ▼
ResearchResponse
       │
       ▼
HTTP 200 Response
```

This separation demonstrates an important backend principle:

> The router handles the HTTP layer while the service handles the application logic.

---

# Technology Stack

| Technology       | Purpose                           |
| ---------------- | --------------------------------- |
| Python           | Programming language              |
| FastAPI          | Web API framework                 |
| Pydantic         | Data validation and schemas       |
| Uvicorn          | ASGI server                       |
| Python `asyncio` | Simulated asynchronous processing |

---

# What This Project Does Not Use

To keep the learning scope focused, this project intentionally does **not** include:

* OpenAI API
* Gemini API
* Groq API
* LangChain
* LangGraph
* Vector databases
* RAG
* PostgreSQL
* MongoDB
* Authentication
* Authorization
* Docker
* Frontend
* Cloud deployment

These technologies are relevant to larger AI applications but are outside the scope of this particular project.

---

# Future Extensions

The current architecture provides a foundation that could later be extended with:

```text
Current Project
      │
      ├── Persistent Database
      │
      ├── Authentication
      │
      ├── Background Tasks
      │
      ├── Middleware
      │
      ├── Automated Testing
      │
      ├── LLM Integration
      │
      ├── RAG Pipeline
      │
      ├── AI Agents
      │
      └── Production Deployment
```

These are intentionally kept separate from the current learning project so that each concept can be understood independently before being combined into a larger system.

---

# Learning Context

This project is part of a broader progression toward **AI Engineering and Agentic AI development**.

The learning progression includes:

```text
LLM Fundamentals
       ↓
Agent Fundamentals
       ↓
RAG + Vector Databases
       ↓
LangChain
       ↓
n8n / AI Automation
       ↓
MCP
       ↓
FastAPI
       ↓
LangGraph
       ↓
Production AI Systems
```

FastAPI is particularly important in this progression because AI applications frequently need a backend layer to expose AI capabilities through reliable HTTP APIs.

For example, a future application could look like:

```text
Flutter Client
      │
      ▼
FastAPI
      │
      ├── Authentication
      │
      ├── API Routes
      │
      ├── Background Jobs
      │
      ▼
LangGraph / LangChain
      │
      ├── Agents
      ├── Tools
      ├── RAG
      └── MCP
      │
      ▼
LLM / External Services
```

This project focuses only on the **FastAPI layer** of that larger architecture.

---

# Key Takeaways

By completing this project, the following FastAPI concepts were implemented and practiced:

* FastAPI application initialization
* Application structure
* `APIRouter`
* Route registration
* HTTP methods
* Path parameters
* Request bodies
* Pydantic models
* Field validation
* Response models
* HTTP status codes
* `HTTPException`
* Dependency Injection
* HTTP headers
* UUID generation
* Async endpoints
* Async service functions
* In-memory state
* Separation of routers and services
* Swagger/OpenAPI documentation

The project intentionally prioritizes **understanding the framework and its architecture** over adding unnecessary technologies.

---

# License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
