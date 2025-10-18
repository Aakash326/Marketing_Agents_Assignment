"""
Health check endpoint for the API.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        JSONResponse with status and message
    """
    logger.info("Health check endpoint called")
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "message": "Portfolio Intelligence API is running",
            "version": "1.0.0"
        }
    )
