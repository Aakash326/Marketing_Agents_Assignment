"""
FastAPI application for LangGraph Portfolio Intelligence API.
"""

import logging
import sys
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

# Add project root to Python path BEFORE importing any routes
# Path: backends/langgraph_backend/app/main.py
# Go up: app -> langgraph_backend -> backends -> PROJECT_ROOT (3 levels)
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
    print(f"Added project root to sys.path: {project_root}")

from app.config import settings, validate_settings
from app.api.routes import query, portfolio, health, stock_analysis, websocket, session, rag
from app.middleware.error_handler import setup_exception_handlers
from app.middleware.logging_middleware import LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Portfolio Intelligence API powered by LangGraph multi-agent system",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)

# Setup exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(query.router, prefix="/api", tags=["Query"])
app.include_router(portfolio.router, prefix="/api", tags=["Portfolio"])
app.include_router(stock_analysis.router, prefix="/api", tags=["Stock Analysis"])
app.include_router(session.router, prefix="/api", tags=["Sessions"])
app.include_router(websocket.router, tags=["WebSocket"])
app.include_router(rag.router, prefix="/api", tags=["RAG"])


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    try:
        # Validate settings
        validate_settings()
        logger.info("Configuration validated successfully")

        # Initialize services (they will be created on first use)
        logger.info("Services ready for initialization on first request")

    except Exception as e:
        logger.error(f"Startup validation failed: {str(e)}")
        # Don't raise to allow app to start, but log the error
        logger.warning("Application started with configuration warnings")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info(f"Shutting down {settings.APP_NAME}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
