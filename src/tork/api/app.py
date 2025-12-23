"""
FastAPI Application

REST API for governance operations.
"""

from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str
    version: str


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Tork Governance API",
        description="REST API for AI agent governance operations",
        version="0.1.0",
    )
    
    @app.get("/health", response_model=HealthResponse)
    async def health_check() -> HealthResponse:
        """Health check endpoint."""
        return HealthResponse(status="healthy", version="0.1.0")
    
    @app.get("/")
    async def root() -> dict:
        """Root endpoint."""
        return {
            "name": "Tork Governance API",
            "version": "0.1.0",
            "docs": "/docs",
        }
    
    return app


app = create_app()
