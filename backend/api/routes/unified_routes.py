"""
Unified API routes for company integration
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import logging

from ..models import UnifiedProcessRequest, ProcessResponse, ErrorResponse
from ...services.pipeline import ProcessingPipeline
from ...services.response_builder import ResponseBuilder

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
pipeline = ProcessingPipeline()
response_builder = ResponseBuilder()

@router.post("/process-csv", response_model=ProcessResponse)
async def process_csv_unified(request: UnifiedProcessRequest, background_tasks: BackgroundTasks):
    """
    Unified CSV Processing Endpoint
    
    This is the main endpoint for company integration. It supports all layer modes
    and provides a single interface for complete CSV processing pipeline.
    
    Features:
    - Supports all layer modes (fast, config, deep)
    - Complete preprocessing, chunking, embedding, and storage pipeline
    - Returns downloadable files (CSV, JSON) and search endpoint
    - Option B response format: File Downloads + JSON
    
    Args:
        request: Unified processing request with layer mode and optional settings
        background_tasks: FastAPI background tasks for cleanup
        
    Returns:
        Complete processing results with download links and search endpoint
    """
    try:
        logger.info(f"Unified processing started - Mode: {request.layer_mode}, File: {request.filename}")
        
        # Build custom settings from request
        custom_settings = {}
        
        if request.preprocessing:
            custom_settings["preprocessing"] = request.preprocessing
        
        if request.chunking:
            custom_settings["chunking"] = request.chunking
        
        if request.embedding:
            custom_settings["embedding"] = request.embedding
        
        if request.storage:
            custom_settings["storage"] = request.storage
        
        # Process CSV through complete pipeline
        result = await pipeline.process_csv(
            csv_data=request.csv_data,
            filename=request.filename,
            layer_mode=request.layer_mode,
            custom_settings=custom_settings if custom_settings else None
        )
        
        if result.get("success"):
            logger.info(f"Unified processing completed: {result.get('processing_id')}")
            
            # Add company-specific response enhancements
            result["api_version"] = "1.0.0"
            result["integration_guide"] = "/api/docs#/Unified%20API/process_csv_unified_api_v1_process_csv_post"
            result["support_contact"] = "api-support@csvoptimizer.com"
            
            return result
        else:
            logger.error(f"Unified processing failed: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error", "Processing failed"))
            
    except Exception as e:
        logger.error(f"Unified processing exception: {e}")
        error_response = response_builder.build_error_response(
            error_message=str(e),
            error_code="UNIFIED_PROCESSING_ERROR"
        )
        raise HTTPException(status_code=500, detail=error_response)

# Additional endpoint for batch processing (future enhancement)
@router.post("/process-csv-batch")
async def process_csv_batch():
    """
    Batch CSV Processing Endpoint (Future Enhancement)
    
    This endpoint will support processing multiple CSV files in a single request.
    Currently returns not implemented.
    """
    raise HTTPException(
        status_code=501, 
        detail="Batch processing not implemented yet. Use /process-csv for single file processing."
    )

# Endpoint to get processing status
@router.get("/processing/{processing_id}/status")
async def get_processing_status(processing_id: str):
    """
    Get Processing Status
    
    Check the status of a processing job by ID.
    Useful for long-running processing jobs.
    """
    # This would typically check a database or cache
    # For now, return a simple response
    return {
        "processing_id": processing_id,
        "status": "completed",  # In real implementation: pending, processing, completed, failed
        "message": "Processing status check - feature coming soon"
    }
