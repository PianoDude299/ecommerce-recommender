"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.config import get_settings
from app.database import init_db

settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    description="AI-Powered E-commerce Product Recommender with LLM Explanations",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()
    print("✅ Database initialized")
    print(f"✅ {settings.project_name} API is running!")
    print(f"📚 API Documentation: http://localhost:8000/docs")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.project_name,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "api": settings.api_v1_prefix
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2025-10-17"
    }


# Include API routes
app.include_router(api_router, prefix=settings.api_v1_prefix)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )