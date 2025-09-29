"""
Main FastAPI application
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import logging
from pathlib import Path

from config.settings import settings
from config.logging import setup_logging
from .models import *
from .routes.layer_routes import router as layer_router
from .routes.unified_routes import router as unified_router
from .routes.download_routes import router as download_router
from .routes.search_routes import router as search_router

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Add trusted host middleware (optional security)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure as needed
)

# Include routers
app.include_router(layer_router, prefix="/api/v1", tags=["Layer APIs"])
app.include_router(unified_router, prefix="/api/v1", tags=["Unified API"])
app.include_router(download_router, prefix="/api/v1", tags=["Downloads"])
app.include_router(search_router, prefix="/api/v1", tags=["Search"])

# Health check endpoint
@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from ..services.response_builder import ResponseBuilder
    response_builder = ResponseBuilder()
    return response_builder.build_health_response()

# API info endpoint
@app.get("/api/v1/info", response_model=InfoResponse)
async def api_info():
    """API information endpoint"""
    from ..services.response_builder import ResponseBuilder
    response_builder = ResponseBuilder()
    return response_builder.build_info_response()

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CSV Chunking Optimizer Pro API",
        "version": settings.VERSION,
        "docs": "/api/docs",
        "health": "/api/v1/health",
        "info": "/api/v1/info"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Server will run on {settings.HOST}:{settings.PORT}")
    
    # Ensure directories exist
    settings.TEMP_FILES_DIR.mkdir(parents=True, exist_ok=True)
    settings.DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
    settings.CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    settings.FAISS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Start background cleanup task
    from ..services.file_handler import FileHandler
    file_handler = FileHandler()
    
    import asyncio
    async def cleanup_task():
        while True:
            try:
                file_handler.cleanup_expired_files()
                await asyncio.sleep(3600)  # Run every hour
            except Exception as e:
                logger.error(f"Cleanup task failed: {e}")
                await asyncio.sleep(3600)
    
    asyncio.create_task(cleanup_task())

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown tasks"""
    logger.info("Shutting down CSV Chunking Optimizer Pro API")

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    from ..services.response_builder import ResponseBuilder
    response_builder = ResponseBuilder()
    
    return response_builder.build_error_response(
        error_message=exc.detail,
        error_code=str(exc.status_code)
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    from ..services.response_builder import ResponseBuilder
    response_builder = ResponseBuilder()
    
    logger.error(f"Unhandled exception: {exc}")
    
    return response_builder.build_error_response(
        error_message="Internal server error",
        error_code="500"
    )

# Development server function
def run_development_server():
    """Run development server"""
    uvicorn.run(
        "backend.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )

if __name__ == "__main__":
    run_development_server()
