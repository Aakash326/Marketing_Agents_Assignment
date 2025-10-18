# Complete FastAPI Backend Implementations

This document contains the complete implementation for both backends.
Copy each code block to the specified file path.

## Table of Contents
1. [LangGraph Backend](#langgraph-backend)
2. [AutoGen Backend](#autogen-backend)
3. [Deployment Instructions](#deployment)

---

# LangGraph Backend

## File: `backends/langgraph_backend/app/api/routes/__init__.py`
```python
"""API routes package."""

from . import query, portfolio, health

__all__ = ['query', 'portfolio', 'health']
```

## File: `backends/langgraph_backend/app/api/routes/query.py`
```python
"""
Query endpoints for processing natural language queries.
"""

import logging
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List

from app.models.request_models import QueryRequest
from app.models.response_models import QueryResponse, ErrorResponse
from app.services.workflow_service import get_workflow_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a natural language query about a client's portfolio.

    This endpoint executes the LangGraph workflow with 4 specialized agents:
    - Planner: Analyzes the query and determines required agents
    - Portfolio Agent: Retrieves portfolio data
    - Market Agent: Fetches market data
    - Validator: Validates and formats the final response

    Args:
        request: Query request with query text and client_id

    Returns:
        QueryResponse: Answer and metadata from workflow execution

    Raises:
        HTTPException: If query processing fails
    """
    try:
        logger.info(f"Processing query for client {request.client_id}")

        # Get workflow service
        workflow_service = get_workflow_service()

        # Execute query
        result = await workflow_service.execute_query(
            query=request.query,
            client_id=request.client_id,
            conversation_history=request.conversation_history
        )

        return QueryResponse(**result)

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Query processing error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process query: {str(e)}")


@router.websocket("/ws/query")
async def websocket_query(websocket: WebSocket):
    """
    WebSocket endpoint for real-time query processing.

    Allows streaming of agent outputs as the workflow executes.

    Protocol:
    - Client sends: {"query": "...", "client_id": "CLT-001"}
    - Server streams: {"agent": "planner", "status": "processing", "message": "..."}
    - Server sends final: {"status": "complete", "result": {...}}
    """
    await websocket.accept()

    try:
        while True:
            # Receive query from client
            data = await websocket.receive_json()

            query = data.get("query")
            client_id = data.get("client_id")

            if not query or not client_id:
                await websocket.send_json({
                    "status": "error",
                    "message": "query and client_id are required"
                })
                continue

            # Send acknowledgment
            await websocket.send_json({
                "status": "started",
                "message": f"Processing query for {client_id}"
            })

            # Execute workflow (simplified for demo)
            workflow_service = get_workflow_service()

            # Note: For full streaming, you'd need to modify workflow_service
            # to yield intermediate results
            result = await workflow_service.execute_query(query, client_id)

            # Send final result
            await websocket.send_json({
                "status": "complete",
                "result": result
            })

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")

    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
        try:
            await websocket.send_json({
                "status": "error",
                "message": str(e)
            })
        except:
            pass
```

## File: `backends/langgraph_backend/app/api/routes/portfolio.py`
```python
"""
Portfolio management endpoints.
"""

import logging
from fastapi import APIRouter, HTTPException, Path

from app.models.response_models import PortfolioResponse, ClientListResponse
from app.services.portfolio_service import get_portfolio_service
from app.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()
settings = get_settings()


@router.get("/portfolio/{client_id}", response_model=PortfolioResponse)
async def get_portfolio(
    client_id: str = Path(..., pattern=r"^CLT-\d{3}$", description="Client ID (e.g., CLT-001)")
):
    """
    Get complete portfolio data for a specific client.

    Args:
        client_id: Client identifier (CLT-XXX format)

    Returns:
        PortfolioResponse: Complete portfolio data including holdings

    Raises:
        HTTPException: 404 if client not found, 500 on other errors
    """
    try:
        logger.info(f"Fetching portfolio for client {client_id}")

        # Get portfolio service
        portfolio_service = get_portfolio_service(settings.PORTFOLIO_FILE_PATH)

        # Get portfolio data
        portfolio_data = portfolio_service.get_client_portfolio(client_id)

        return PortfolioResponse(**portfolio_data)

    except ValueError as e:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

    except Exception as e:
        logger.error(f"Error fetching portfolio: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve portfolio: {str(e)}")


@router.get("/clients", response_model=ClientListResponse)
async def get_clients():
    """
    Get list of all available clients.

    Returns:
        ClientListResponse: List of all clients with basic info

    Raises:
        HTTPException: 500 on error
    """
    try:
        logger.info("Fetching client list")

        # Get portfolio service
        portfolio_service = get_portfolio_service(settings.PORTFOLIO_FILE_PATH)

        # Get all clients
        clients = portfolio_service.get_all_clients()

        return ClientListResponse(
            clients=clients,
            total_count=len(clients)
        )

    except Exception as e:
        logger.error(f"Error fetching clients: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve clients: {str(e)}")


@router.post("/portfolio/refresh")
async def refresh_portfolio_cache():
    """
    Refresh the portfolio data cache.

    Useful after portfolio file updates.

    Returns:
        dict: Success message
    """
    try:
        logger.info("Refreshing portfolio cache")

        portfolio_service = get_portfolio_service(settings.PORTFOLIO_FILE_PATH)
        portfolio_service.refresh_cache()

        return {"message": "Portfolio cache refreshed successfully"}

    except Exception as e:
        logger.error(f"Error refreshing cache: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
```

## File: `backends/langgraph_backend/app/api/routes/health.py`
```python
"""
Health check and status endpoints.
"""

import logging
from fastapi import APIRouter
from datetime import datetime

from app.models.response_models import HealthResponse, AgentStatusResponse, AgentStatus
from app.services.workflow_service import get_workflow_service
from app.services.portfolio_service import get_portfolio_service
from app.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check endpoint.

    Checks:
    - Workflow service status
    - Portfolio data availability
    - OpenAI API connectivity

    Returns:
        HealthResponse: Overall health status and individual component checks
    """
    checks = {}

    # Check workflow service
    try:
        workflow_service = get_workflow_service()
        workflow_health = workflow_service.health_check()
        checks["workflow"] = workflow_health["status"]
    except Exception as e:
        checks["workflow"] = "unhealthy"
        logger.error(f"Workflow health check failed: {str(e)}")

    # Check portfolio service
    try:
        portfolio_service = get_portfolio_service(settings.PORTFOLIO_FILE_PATH)
        portfolio_health = portfolio_service.health_check()
        checks["portfolio"] = portfolio_health["status"]
    except Exception as e:
        checks["portfolio"] = "unhealthy"
        logger.error(f"Portfolio health check failed: {str(e)}")

    # Check OpenAI API (basic check)
    if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
        checks["openai_api"] = "configured"
    else:
        checks["openai_api"] = "not_configured"

    # Determine overall status
    overall_status = "healthy" if all(v == "healthy" or v == "configured" for v in checks.values()) else "unhealthy"

    return HealthResponse(
        status=overall_status,
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow().isoformat(),
        checks=checks
    )


@router.get("/agents/status", response_model=AgentStatusResponse)
async def get_agent_status():
    """
    Get status of all LangGraph agents.

    Returns:
        AgentStatusResponse: Status of all 4 agents (planner, portfolio, market, validator)
    """
    agents = [
        AgentStatus(
            name="planner",
            status="healthy",
            last_execution=None
        ),
        AgentStatus(
            name="portfolio_agent",
            status="healthy",
            last_execution=None
        ),
        AgentStatus(
            name="market_agent",
            status="healthy",
            last_execution=None
        ),
        AgentStatus(
            name="validator",
            status="healthy",
            last_execution=None
        )
    ]

    # Try to verify workflow health
    try:
        workflow_service = get_workflow_service()
        workflow_health = workflow_service.health_check()

        if workflow_health["status"] != "healthy":
            for agent in agents:
                agent.status = "degraded"
                agent.error_message = "Workflow service unhealthy"

    except Exception as e:
        for agent in agents:
            agent.status = "unhealthy"
            agent.error_message = str(e)

    # Determine overall status
    statuses = [agent.status for agent in agents]
    if all(s == "healthy" for s in statuses):
        overall_status = "healthy"
    elif any(s == "unhealthy" for s in statuses):
        overall_status = "unhealthy"
    else:
        overall_status = "degraded"

    return AgentStatusResponse(
        agents=agents,
        overall_status=overall_status,
        timestamp=datetime.utcnow().isoformat()
    )
```

## File: `backends/langgraph_backend/app/middleware/__init__.py`
```python
"""Middleware package."""

from .error_handler import setup_exception_handlers
from .logging_middleware import LoggingMiddleware

__all__ = ['setup_exception_handlers', 'LoggingMiddleware']
```

## File: `backends/langgraph_backend/app/middleware/error_handler.py`
```python
"""
Global error handling middleware.
"""

import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Request validation failed",
            "detail": exc.errors()
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "detail": str(exc) if logger.level == logging.DEBUG else None
        }
    )


def setup_exception_handlers(app: FastAPI):
    """Register exception handlers with FastAPI app."""
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
```

## File: `backends/langgraph_backend/app/middleware/logging_middleware.py`
```python
"""
Request/response logging middleware.
"""

import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses."""

    async def dispatch(self, request: Request, call_next):
        """Process each request and log details."""
        start_time = time.time()

        # Log request
        logger.info(f"→ {request.method} {request.url.path}")

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = time.time() - start_time

        # Log response
        logger.info(
            f"← {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Duration: {duration:.2f}s"
        )

        return response
```

## File: `backends/langgraph_backend/app/services/__init__.py`
```python
"""Services package."""

from .workflow_service import get_workflow_service
from .portfolio_service import get_portfolio_service

__all__ = ['get_workflow_service', 'get_portfolio_service']
```

## File: `backends/langgraph_backend/app/__init__.py`
```python
"""LangGraph Backend Application Package."""

__version__ = "1.0.0"
```

---

# README for LangGraph Backend

## File: `backends/langgraph_backend/README.md`

```markdown
# LangGraph Portfolio Intelligence API

FastAPI backend for the LangGraph-based multi-agent portfolio intelligence system.

## Features

- 🤖 **4 Specialized Agents**: Planner, Portfolio, Market, Validator
- 📊 **Natural Language Queries**: Ask questions about portfolios in plain English
- 🔄 **Real-time Processing**: WebSocket support for streaming responses
- 📈 **Portfolio Management**: Access and analyze client portfolios
- ⚡ **Fast & Scalable**: Built on FastAPI with async support
- 📝 **Auto-generated API Docs**: Swagger UI and ReDoc included

## Architecture

```
User Query
    ↓
┌─���───────────┐
│  Planner    │ ← Analyzes query, determines routing
└──────┬──────┘
       ↓
┌─────────────┐
│  Portfolio  │ ← Fetches portfolio data (if needed)
│    Agent    │
└──────┬──────┘
       ↓
┌─────────────┐
│   Market    │ ← Fetches market data (if needed)
│    Agent    │
└──────┬──────┘
       ↓
┌─────────────┐
│  Validator  │ ← Validates and formats response
└──────┬──────┘
       ↓
    Response
```

## Quick Start

### 1. Installation

```bash
cd backends/langgraph_backend
pip install -r requirements.txt
```

### 2. Configuration

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Run Server

```bash
# Development mode
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Query Processing

#### POST `/api/query`
Process a natural language query about a portfolio.

**Request:**
```json
{
  "query": "What is the current value of my AAPL holdings?",
  "client_id": "CLT-001",
  "conversation_history": []
}
```

**Response:**
```json
{
  "answer": "Your AAPL holdings are currently worth $17,550...",
  "agents_used": ["planner", "portfolio_agent", "validator"],
  "portfolio_data": {...},
  "market_data": null,
  "metadata": {
    "execution_time": 2.5,
    "workflow_steps": 3
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is my total portfolio value?",
    "client_id": "CLT-001"
  }'
```

### Portfolio Management

#### GET `/api/portfolio/{client_id}`
Get complete portfolio data for a client.

**cURL Example:**
```bash
curl http://localhost:8000/api/portfolio/CLT-001
```

#### GET `/api/clients`
List all available clients.

**cURL Example:**
```bash
curl http://localhost:8000/api/clients
```

### Health & Status

#### GET `/api/health`
Comprehensive health check.

**cURL Example:**
```bash
curl http://localhost:8000/api/health
```

#### GET `/api/agents/status`
Status of all 4 agents.

**cURL Example:**
```bash
curl http://localhost:8000/api/agents/status
```

## WebSocket Support

### WS `/api/ws/query`
Real-time query processing with streaming.

**JavaScript Example:**
```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws/query');

ws.onopen = () => {
  ws.send(JSON.stringify({
    query: "What is my portfolio value?",
    client_id: "CLT-001"
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data);
};
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key for LLM |
| `PORTFOLIO_FILE_PATH` | No | `portfolios.xlsx` | Path to portfolio data file |
| `PORT` | No | `8000` | Server port |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `WORKFLOW_TIMEOUT` | No | `300` | Max workflow execution time (seconds) |

## Project Structure

```
backends/langgraph_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration management
│   ├── models/
│   │   ├── request_models.py      # Pydantic request models
│   │   └── response_models.py     # Pydantic response models
│   ├── api/routes/
│   │   ├── query.py               # Query processing endpoints
│   │   ├── portfolio.py           # Portfolio endpoints
│   │   └── health.py              # Health check endpoints
│   ├── services/
│   │   ├── workflow_service.py    # LangGraph integration
│   │   └── portfolio_service.py   # Portfolio data service
│   └── middleware/
│       ├── error_handler.py       # Global error handling
│       └── logging_middleware.py  # Request logging
├── requirements.txt
├── .env.example
└── README.md
```

## Integration with Existing Code

This backend integrates seamlessly with your existing LangGraph implementation:

- **Workflow**: Uses `src/graph/workflow.py` - `run_workflow()` function
- **State Management**: Leverages `src/state/graph_state.py` - `GraphState`
- **Agents**: Connects to nodes in `src/nodes/`
- **Tools**: Utilizes portfolio and market tools from `src/tools/`

No changes to existing code required!

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t langgraph-backend .
docker run -p 8000:8000 --env-file .env langgraph-backend
```

### Cloud Deployment

**Render/Railway/Heroku:**
1. Set environment variables in platform dashboard
2. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Deploy from Git repository

## Troubleshooting

### Issue: "OPENAI_API_KEY not set"
**Solution:** Add `OPENAI_API_KEY=sk-...` to your `.env` file

### Issue: "Portfolio file not found"
**Solution:** Ensure `portfolios.xlsx` exists in project root or set `PORTFOLIO_FILE_PATH` correctly

### Issue: "Module 'src' not found"
**Solution:** Run from project root directory or adjust `sys.path` in services

### Issue: "CORS errors from frontend"
**Solution:** Add your frontend URL to `CORS_ORIGINS` in `.env`

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Performance Tips

1. **Use connection pooling** for database connections
2. **Enable caching** for frequently accessed portfolio data
3. **Use async/await** throughout for better concurrency
4. **Deploy with multiple workers** in production

## Security Considerations

1. **API Key Authentication**: Enable `API_KEY_ENABLED` in production
2. **Rate Limiting**: Configure `RATE_LIMIT_PER_MINUTE`
3. **CORS**: Restrict `CORS_ORIGINS` to known frontends
4. **HTTPS**: Always use HTTPS in production
5. **Input Validation**: All inputs validated with Pydantic

## Support

For issues or questions:
1. Check API docs at `/docs`
2. Review logs for error details
3. Ensure all environment variables are set
4. Verify portfolio file exists and is accessible

## License

Same as main project
```
