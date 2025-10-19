"""
FastAPI application for AutoGen 6-Agent Stock Analysis System
"""

import logging
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, PROJECT_ROOT)

from app.api import stock_analysis

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AutoGen 6-Agent Stock Analysis API",
    version="1.0.0",
    description="Stock analysis powered by AutoGen multi-agent system",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stock_analysis.router, prefix="/api", tags=["Stock Analysis"])


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting AutoGen 6-Agent Stock Analysis API v1.0.0")
    logger.info("API Documentation available at /docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down AutoGen 6-Agent Stock Analysis API")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": "AutoGen 6-Agent Stock Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "AutoGen 6-Agent API is running",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
