# FastAPI Backend - Quick Start Guide

Get the Portfolio Intelligence API running in 5 minutes.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# From project root
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- All existing dependencies

### 2. Start the Server

```bash
cd backend
python main.py
```

You should see:
```
🚀 Starting Portfolio Intelligence API
Version: 1.0.0
...
✨ Portfolio Intelligence API is ready
📖 API Documentation: http://0.0.0.0:8000/docs
```

### 3. Test It Works

Open a new terminal and run:

```bash
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "service": "portfolio-intelligence-api",
  "version": "1.0.0",
  "active_sessions": 0
}
```

### 4. Try a Query

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What stocks do I own?",
    "client_id": "CLT-001"
  }'
```

### 5. View Documentation

Open your browser to:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📖 Example API Calls

### Get Portfolio Holdings

```bash
curl http://localhost:8000/api/v1/clients/CLT-001/portfolio
```

### Ask About Performance

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Which of my holdings has the best return?",
    "client_id": "CLT-001"
  }'
```

### Get Market Data

```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the current price of AAPL?",
    "client_id": "CLT-001"
  }'
```

## 🧪 Run Tests

```bash
cd backend
python test_api.py
```

This will test all endpoints and verify everything works.

## 🛑 Troubleshooting

### Port 8000 Already in Use

Kill the process:
```bash
lsof -ti:8000 | xargs kill -9
```

Or use a different port:
```bash
uvicorn main:app --port 8001
```

### Import Errors

Make sure you're in the backend directory:
```bash
cd backend
python main.py
```

### OpenAI API Key Error

Create `.env` file in project root:
```bash
echo 'OPENAI_API_KEY=your-key-here' > ../.env
```

## 📚 Next Steps

1. Read `backend/README.md` for detailed documentation
2. Explore interactive API docs at http://localhost:8000/docs
3. Try the example curl commands above
4. Build a frontend client using the API

## 🔗 Available Clients

- CLT-001, CLT-002, CLT-003, CLT-004, CLT-005
- CLT-007, CLT-009, CLT-010

## 💡 Tips

- Use `/docs` for interactive testing in the browser
- Session IDs are automatically generated
- Conversation history is maintained per session
- Sessions auto-cleanup after 24 hours of inactivity

---

**That's it! Your API is ready to use. 🎉**

For more details, see `backend/README.md`
