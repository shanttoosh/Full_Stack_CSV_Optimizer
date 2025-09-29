"""
Layer-wise API routes (Layer 1, 2, 3)
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import logging

from ..models import Layer1ProcessRequest, Layer2ProcessRequest, Layer3ProcessRequest, ProcessResponse, ErrorResponse
from ...services.pipeline import ProcessingPipeline
from ...services.response_builder import ResponseBuilder
from ...utils.helpers import get_layer_defaults, merge_settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
pipeline = ProcessingPipeline()
response_builder = ResponseBuilder()

@router.post("/layer1/process", response_model=ProcessResponse)
async def process_layer1(request: Layer1ProcessRequest, background_tasks: BackgroundTasks):
    """
    Layer 1 (Fast Mode) Processing
    - Auto-optimized defaults
    - Minimal configuration required
    - Fast processing with basic chunking and embedding
    """
    try:
        logger.info(f"Layer 1 processing started for file: {request.filename}")
        
        # Use fast mode defaults
        result = await pipeline.process_csv(
            csv_data=request.csv_data,
            filename=request.filename,
            layer_mode="fast",
            custom_settings=None  # Use all defaults
        )
        
        if result.get("success"):
            logger.info(f"Layer 1 processing completed: {result.get('processing_id')}")
            return result
        else:
            logger.error(f"Layer 1 processing failed: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error", "Processing failed"))
            
    except Exception as e:
        logger.error(f"Layer 1 processing exception: {e}")
        error_response = response_builder.build_error_response(
            error_message=str(e),
            error_code="LAYER1_PROCESSING_ERROR"
        )
        raise HTTPException(status_code=500, detail=error_response)

@router.post("/layer2/process", response_model=ProcessResponse)
async def process_layer2(request: Layer2ProcessRequest, background_tasks: BackgroundTasks):
    """
    Layer 2 (Config Mode) Processing
    - Medium configuration level
    - User can specify chunking method, embedding model, batch size
    - Balanced between speed and customization
    """
    try:
        logger.info(f"Layer 2 processing started for file: {request.filename}")
        
        # Build custom settings from request
        custom_settings = {}
        
        if request.chunking_method:
            custom_settings["chunking"] = {"method": request.chunking_method}
        
        if request.embedding_model:
            custom_settings["embedding"] = {"model": request.embedding_model}
        
        if request.batch_size:
            if "embedding" not in custom_settings:
                custom_settings["embedding"] = {}
            custom_settings["embedding"]["batch_size"] = request.batch_size
        
        result = await pipeline.process_csv(
            csv_data=request.csv_data,
            filename=request.filename,
            layer_mode="config",
            custom_settings=custom_settings
        )
        
        if result.get("success"):
            logger.info(f"Layer 2 processing completed: {result.get('processing_id')}")
            return result
        else:
            logger.error(f"Layer 2 processing failed: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error", "Processing failed"))
            
    except Exception as e:
        logger.error(f"Layer 2 processing exception: {e}")
        error_response = response_builder.build_error_response(
            error_message=str(e),
            error_code="LAYER2_PROCESSING_ERROR"
        )
        raise HTTPException(status_code=500, detail=error_response)

@router.post("/layer3/process", response_model=ProcessResponse)
async def process_layer3(request: Layer3ProcessRequest, background_tasks: BackgroundTasks):
    """
    Layer 3 (Deep Config Mode) Processing
    - Full configuration control
    - User can specify all processing parameters
    - Maximum customization and control
    """
    try:
        logger.info(f"Layer 3 processing started for file: {request.filename}")
        
        # Use deep config settings from request
        custom_settings = {}
        
        if request.preprocessing:
            custom_settings["preprocessing"] = request.preprocessing
        
        if request.chunking:
            custom_settings["chunking"] = request.chunking
        
        if request.embedding:
            custom_settings["embedding"] = request.embedding
        
        if request.storage:
            custom_settings["storage"] = request.storage
        
        result = await pipeline.process_csv(
            csv_data=request.csv_data,
            filename=request.filename,
            layer_mode="deep",
            custom_settings=custom_settings
        )
        
        if result.get("success"):
            logger.info(f"Layer 3 processing completed: {result.get('processing_id')}")
            return result
        else:
            logger.error(f"Layer 3 processing failed: {result.get('error')}")
            raise HTTPException(status_code=500, detail=result.get("error", "Processing failed"))
            
    except Exception as e:
        logger.error(f"Layer 3 processing exception: {e}")
        error_response = response_builder.build_error_response(
            error_message=str(e),
            error_code="LAYER3_PROCESSING_ERROR"
        )
        raise HTTPException(status_code=500, detail=error_response)
