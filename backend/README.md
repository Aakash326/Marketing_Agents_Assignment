# Portfolio Intelligence API - FastAPI Backend

RESTful API backend for the Portfolio Intelligence System, exposing multi-agent workflow capabilities through clean HTTP endpoints.

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Running the API](#running-the-api)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Development](#development)

## 🎯 Overview

This FastAPI backend wraps the existing LangGraph multi-agent portfolio intelligence system, providing:

- ✅ RESTful API endpoints
- ✅ Session management and conversation history
- ✅ Structured JSON request/response models
- ✅ Automatic API documentation (OpenAPI/Swagger)
- ✅ Async operations for scalability
- ✅ Comprehensive error handling
- ✅ CORS support for web clients

## 🏗 Architecture

```
backend/
├── main.py                    # FastAPI app entry point
├── config.py                  # Configuration settings
├── api/
│   ├── routes.py              # API endpoint definitions
│   └── models.py              # Pydantic request/response models
├── services/
│   ├── workflow_service.py    # Workflow execution wrapper
│   └── session_service.py     # Session/history management
└── utils/                     # Utility modules
```

### Key Components

1. **FastAPI Application** (`main.py`)
   - Lifecycle management (startup/shutdown)
   - CORS middleware
   - Global exception handling
   - Service initialization

2. **API Routes** (`api/routes.py`)
   - Query portfolio endpoint
   - Clarification handling
   - Session management
   - Portfolio retrieval

3. **Services**
   - `WorkflowService`: Wraps LangGraph workflow execution
   - `SessionService`: In-memory session and conversation history management

4. **Models** (`api/models.py`)
   - Pydantic models for type-safe request/response validation
   - Automatic OpenAPI schema generation

## 📦 Installation

### Prerequisites

- Python 3.11+
- All dependencies from root `requirements.txt`

### Install Dependencies

From the project root:

```bash
pip install -r requirements.txt
```

Or just the FastAPI dependencies:

```bash
pip install fastapi==0.109.0 uvicorn[standard]==0.27.0 pydantic==2.5.3 pydantic-settings==2.1.0
```

### Environment Setup

Ensure your `.env` file in the project root contains:

```bash
OPENAI_API_KEY=your-api-key-here
```

## 🚀 Running the API

### Development Mode (with auto-reload)

From the `backend/` directory:

```bash
cd backend
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will start on `http://localhost:8000`

### Verify It's Running

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "portfolio-intelligence-api",
  "version": "1.0.0",
  "active_sessions": 0
}
```

## 📚 API Endpoints

### Interactive Documentation

Visit these URLs when the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

### Endpoints Overview

#### 1. Health Check

```http
GET /health
```

Response:
```json
{
  "status": "healthy",
  "service": "portfolio-intelligence-api",
  "version": "1.0.0",
  "active_sessions": 0
}
```

#### 2. Query Portfolio (Main Endpoint)

```http
POST /api/v1/query
Content-Type: application/json

{
  "query": "What stocks do I own?",
  "client_id": "CLT-001",
  "session_id": null,
  "conversation_history": []
}
```

Response:
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "You own 6 holdings: VTI, BND, VXUS, VYM, VTEB, and CASH...",
  "needs_clarification": false,
  "clarification_message": null,
  "agent_activity": {
    "planner_used": true,
    "portfolio_used": true,
    "market_used": false,
    "collaboration_used": false,
    "validator_used": true
  },
  "metadata": {
    "query_time_ms": 1234,
    "timestamp": "2025-01-15T10:30:00Z"
  }
}
```

#### 3. Clarification Follow-up

```http
POST /api/v1/query/clarify
Content-Type: application/json

{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "clarification": "AAPL",
  "original_query": "How's that stock doing?"
}
```

#### 4. Get Session Details

```http
GET /api/v1/session/{session_id}
```

Response:
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "client_id": "CLT-001",
  "conversation_history": [
    {"role": "user", "content": "What stocks do I own?"},
    {"role": "assistant", "content": "You own 6 holdings..."}
  ],
  "created_at": "2025-01-15T10:00:00",
  "last_activity": "2025-01-15T10:30:00",
  "message_count": 2
}
```

#### 5. Delete Session

```http
DELETE /api/v1/session/{session_id}
```

Response:
```json
{
  "success": true,
  "message": "Session deleted successfully",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 6. Get Client Portfolio

```http
GET /api/v1/clients/{client_id}/portfolio
```

Response:
```json
{
  "client_id": "CLT-001",
  "total_holdings": 6,
  "holdings": [
    {
      "symbol": "VTI",
      "security_name": "Vanguard Total Stock Market ETF",
      "asset_class": "Equity ETF",
      "sector": "Broad Market",
      "quantity": 3500,
      "purchase_price": 121.06,
      "purchase_date": "2024-01-16"
    }
  ]
}
```

## 🧪 Testing

### Using cURL

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Query Portfolio
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What stocks do I own?",
    "client_id": "CLT-001"
  }'
```

#### Get Portfolio
```bash
curl http://localhost:8000/api/v1/clients/CLT-001/portfolio
```

#### Get Session
```bash
curl http://localhost:8000/api/v1/session/YOUR-SESSION-ID
```

### Using Python requests

```python
import requests

# Query portfolio
response = requests.post(
    "http://localhost:8000/api/v1/query",
    json={
        "query": "What stocks do I own?",
        "client_id": "CLT-001"
    }
)
print(response.json())

# Get portfolio
response = requests.get("http://localhost:8000/api/v1/clients/CLT-001/portfolio")
print(response.json())
```

### Using HTTPie

```bash
# Install httpie
pip install httpie

# Query portfolio
http POST localhost:8000/api/v1/query \
  query="What stocks do I own?" \
  client_id="CLT-001"

# Get portfolio
http GET localhost:8000/api/v1/clients/CLT-001/portfolio
```

## 🛠 Development

### Project Structure

The backend is designed to be:
- **Simple**: No over-engineering, clean code
- **Maintainable**: Clear separation of concerns
- **Scalable**: Ready for async operations
- **Production-ready**: Proper error handling and logging

### Design Decisions

1. **In-Memory Sessions**: Currently using dict-based storage for simplicity
   - Can be replaced with Redis/database later
   - Good for development and small-scale deployments

2. **No Authentication Yet**: Intentionally omitted for simplicity
   - Plan to add OAuth2/JWT in future
   - Easy to integrate with FastAPI's security utilities

3. **Minimal Changes to src/**: Workflow code remains unchanged
   - Backend wraps existing functionality
   - Easy to maintain both Streamlit and API versions

4. **Async-Ready**: Using `async def` for scalability
   - Can handle concurrent requests efficiently
   - Ready for async database operations

### Adding New Endpoints

1. Define Pydantic models in `api/models.py`
2. Add route handler in `api/routes.py`
3. Update this README with examples

### Configuration

Edit `config.py` to modify:
- API version and metadata
- CORS origins
- Session cleanup settings
- Server host/port

## 📝 Notes

### Current Limitations

- ❌ No authentication/authorization (coming soon)
- ❌ No database persistence (using in-memory storage)
- ❌ No rate limiting
- ❌ No request caching

### Future Enhancements

- [ ] Add OAuth2/JWT authentication
- [ ] Integrate Redis for session storage
- [ ] Add request rate limiting
- [ ] Implement response caching
- [ ] Add monitoring/metrics (Prometheus)
- [ ] Containerize with Docker
- [ ] Add CI/CD pipeline

## 🤝 Integration with Existing System

The FastAPI backend works alongside the existing Streamlit app:

- **Streamlit** (`app.py`): User-friendly web interface
- **FastAPI** (`backend/main.py`): RESTful API for programmatic access

Both use the same underlying workflow in `src/graph/workflow.py`.

## 🆘 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001
```

### Module Import Errors

```bash
# Ensure you're in the backend directory
cd backend
python main.py
```

### OpenAI API Key Not Found

Ensure `.env` file exists in project root with:
```
OPENAI_API_KEY=your-key-here
```

## 📄 License

Same as parent project - Internal use only.

---

**Built with ❤️ using FastAPI**
