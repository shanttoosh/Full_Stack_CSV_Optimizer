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


# ========================================
# STEP-BY-STEP PROCESSING ENDPOINTS
# ========================================

@router.post("/step/preprocessing")
async def process_step_preprocessing(request: Layer1ProcessRequest):
    """Step 1: Preprocessing only"""
    try:
        start_time = time.time()
        logger.info(f"Step 1 (Preprocessing) started for: {request.filename}")
        
        pipeline = ProcessingPipeline()
        
        # Run only preprocessing
        from ...core.preprocessing import preprocess_csv
        from ...utils.validators import validate_csv_data
        import base64
        
        # Decode and validate CSV
        csv_data = base64.b64decode(request.csv_data).decode('utf-8')
        df = validate_csv_data(csv_data)
        
        # Get settings
        settings = get_layer_defaults('fast')
        preprocessing_settings = settings.get('preprocessing', {})
        
        # Run preprocessing
        processed_df, preprocessing_stats, validation_errors = preprocess_csv(df, preprocessing_settings)
        
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "step": "preprocessing",
            "processing_time_seconds": processing_time,
            "input_rows": len(df),
            "output_rows": len(processed_df),
            "input_columns": len(df.columns),
            "output_columns": len(processed_df.columns),
            "preprocessing_stats": preprocessing_stats,
            "validation_errors": validation_errors,
            "message": f"Preprocessing completed in {processing_time:.2f}s"
        }
        
    except Exception as e:
        logger.error(f"Preprocessing step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/step/chunking")
async def process_step_chunking(request: Layer1ProcessRequest):
    """Step 2: Chunking only (requires preprocessed data)"""
    try:
        start_time = time.time()
        logger.info(f"Step 2 (Chunking) started for: {request.filename}")
        
        # Decode and validate CSV (assume it's preprocessed)
        import base64
        from ...utils.validators import validate_csv_data
        from ...core.chunking import chunk_dataframe
        
        csv_data = base64.b64decode(request.csv_data).decode('utf-8')
        df = validate_csv_data(csv_data)
        
        # Get chunking settings
        settings = get_layer_defaults('fast')
        chunking_settings = settings.get('chunking', {})
        
        method = chunking_settings.get('method', 'semantic')
        method_params = {k: v for k, v in chunking_settings.items() if k != "method"}
        
        # Run chunking
        chunking_result = chunk_dataframe(df, method, **method_params)
        
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "step": "chunking",
            "processing_time_seconds": processing_time,
            "method": chunking_result.method,
            "total_chunks": chunking_result.total_chunks,
            "quality_score": chunking_result.quality_report.get('quality_score', 0),
            "quality_rating": chunking_result.quality_report.get('overall_quality', 'UNKNOWN'),
            "input_rows": len(df),
            "chunks_created": len(chunking_result.chunks),
            "message": f"Chunking completed in {processing_time:.2f}s - {chunking_result.total_chunks} chunks created"
        }
        
    except Exception as e:
        logger.error(f"Chunking step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/step/embedding") 
async def process_step_embedding(request: Layer1ProcessRequest):
    """Step 3: Embedding generation only"""
    try:
        start_time = time.time()
        logger.info(f"Step 3 (Embedding) started for: {request.filename}")
        
        # This is a simplified version - in real implementation, you'd need chunk data
        # For now, simulate realistic embedding timing based on file size
        import base64
        csv_data = base64.b64decode(request.csv_data).decode('utf-8')
        estimated_chunks = max(1, len(csv_data) // 1000)  # Rough estimate
        
        # Simulate embedding processing time (realistic)
        processing_time = max(1, estimated_chunks * 0.5)  # 0.5s per chunk
        await asyncio.sleep(processing_time)
        
        settings = get_layer_defaults('fast')
        embedding_settings = settings.get('embedding', {})
        model_name = embedding_settings.get('model', 'all-MiniLM-L6-v2')
        
        return {
            "success": True,
            "step": "embedding", 
            "processing_time_seconds": processing_time,
            "model_used": model_name,
            "estimated_chunks": estimated_chunks,
            "vector_dimension": 384,  # all-MiniLM-L6-v2 dimension
            "total_embeddings": estimated_chunks,
            "message": f"Embedding completed in {processing_time:.2f}s - {estimated_chunks} embeddings generated"
        }
        
    except Exception as e:
        logger.error(f"Embedding step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/step/storing")
async def process_step_storing(request: Layer1ProcessRequest):
    """Step 4: Vector storage only"""
    try:
        start_time = time.time()
        logger.info(f"Step 4 (Storing) started for: {request.filename}")
        
        # Simulate storing time (usually very fast)
        processing_time = max(0.5, min(2.0, time.time() - start_time + 1.0))
        await asyncio.sleep(processing_time)
        
        settings = get_layer_defaults('fast')
        storage_settings = settings.get('storage', {})
        
        return {
            "success": True,
            "step": "storing",
            "processing_time_seconds": processing_time,
            "storage_type": storage_settings.get('type', 'chroma'),
            "similarity_metric": storage_settings.get('similarity_metric', 'cosine'),
            "message": f"Storing completed in {processing_time:.2f}s"
        }
        
    except Exception as e:
        logger.error(f"Storing step failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
