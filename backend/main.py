"""
FastAPI application entry point for Portfolio Intelligence API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.api import routes
from backend.api.routes import set_session_service
from backend.services.session_service import SessionService
from backend.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instances
session_service: SessionService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for startup and shutdown events.
    """
    # Startup
    logger.info("=" * 60)
    logger.info("🚀 Starting Portfolio Intelligence API")
    logger.info(f"Version: {settings.VERSION}")
    logger.info(f"API Path: {settings.API_V1_STR}")
    logger.info("=" * 60)
    
    # Initialize services
    global session_service
    session_service = SessionService(max_conversation_history=settings.MAX_CONVERSATION_HISTORY)
    set_session_service(session_service)
    logger.info("✅ Session service initialized")
    
    # Optional: Warm up the workflow (uncomment if needed)
    # logger.info("🔥 Warming up workflow...")
    # try:
    #     from src.graph.workflow import run_workflow
    #     run_workflow("test", "CLT-001", [])
    #     logger.info("✅ Workflow warmed up successfully")
    # except Exception as e:
    #     logger.warning(f"⚠️  Workflow warm-up failed: {e}")
    
    logger.info("=" * 60)
    logger.info("✨ Portfolio Intelligence API is ready")
    logger.info(f"📖 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("=" * 60)
    logger.info("👋 Shutting down Portfolio Intelligence API")
    
    # Cleanup old sessions
    if session_service:
        cleanup_count = session_service.cleanup_old_sessions(hours=0)
        logger.info(f"🧹 Cleaned up {cleanup_count} sessions")
    
    logger.info("✅ Shutdown complete")
    logger.info("=" * 60)


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "status_code": 500
        }
    )


# Include API routes
app.include_router(routes.router, prefix=settings.API_V1_STR)


# Root endpoints
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "documentation": "/docs",
        "health": "/health",
        "api": settings.API_V1_STR
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    active_sessions = session_service.get_session_count() if session_service else 0
    
    return {
        "status": "healthy",
        "service": "portfolio-intelligence-api",
        "version": settings.VERSION,
        "active_sessions": active_sessions
    }


# Development server runner
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting development server on {settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
