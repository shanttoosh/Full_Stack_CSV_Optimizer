"""
Search and retrieval routes
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import logging

from ..models import SearchRequest, SearchResponse, ErrorResponse
from ...services.pipeline import ProcessingPipeline
from ...services.response_builder import ResponseBuilder

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
pipeline = ProcessingPipeline()
response_builder = ResponseBuilder()

@router.post("/search/{processing_id}", response_model=SearchResponse)
async def search_chunks(processing_id: str, request: SearchRequest):
    """
    Search processed chunks
    
    Search through the chunks created during processing using semantic similarity.
    Supports multiple similarity metrics and embedding models.
    
    Args:
        processing_id: Processing session ID from previous processing
        request: Search request with query and parameters
        
    Returns:
        Search results with similarity scores and chunk content
    """
    try:
        logger.info(f"Search request for processing_id: {processing_id}, query: {request.query}")
        
        # Determine storage type (try both)
        # In a production system, this would be stored with the processing job
        store_types_to_try = ["chroma", "faiss"]
        
        result = None
        for store_type in store_types_to_try:
            try:
                result = await pipeline.search_chunks(
                    processing_id=processing_id,
                    query=request.query,
                    model_name=request.model_name,
                    top_k=request.top_k,
                    similarity_metric=request.similarity_metric,
                    store_type=store_type
                )
                
                if result.get("success") and result.get("results"):
                    logger.info(f"Search successful with {store_type}: {len(result.get('results', []))} results")
                    break
                    
            except Exception as e:
                logger.warning(f"Search failed with {store_type}: {e}")
                continue
        
        if not result or not result.get("success"):
            logger.warning(f"Search failed for processing_id: {processing_id}")
            raise HTTPException(
                status_code=404, 
                detail=f"No search results found for processing_id: {processing_id}. The data may have expired or the processing_id may be invalid."
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search exception for processing_id {processing_id}: {e}")
        error_response = response_builder.build_error_response(
            error_message=str(e),
            error_code="SEARCH_ERROR",
            processing_id=processing_id
        )
        raise HTTPException(status_code=500, detail=error_response)

@router.get("/search/{processing_id}/info")
async def get_search_info(processing_id: str):
    """
    Get search information for a processing session
    
    Returns available search configuration and statistics for a processing session.
    
    Args:
        processing_id: Processing session ID
        
    Returns:
        Search configuration and availability information
    """
    try:
        # Check if data exists in either store
        from ...core.storing import get_available_stores
        available_stores = get_available_stores()
        
        search_info = {
            "processing_id": processing_id,
            "available_stores": available_stores,
            "supported_models": [
                "all-MiniLM-L6-v2",
                "BAAI/bge-small-en-v1.5"
            ],
            "supported_similarity_metrics": [
                "cosine",
                "dot", 
                "euclidean"
            ],
            "max_top_k": 100,
            "search_endpoint": f"/api/v1/search/{processing_id}",
            "example_request": {
                "query": "your search query here",
                "model_name": "all-MiniLM-L6-v2",
                "top_k": 5,
                "similarity_metric": "cosine"
            }
        }
        
        # Try to get actual stats from stores
        for store_type in available_stores:
            try:
                from ...core.retrieval import create_retriever
                
                retriever = create_retriever(
                    store_type=store_type,
                    persist_directory=f"./backend/storage/.{store_type}",
                    collection_name="csv_chunks" if store_type == "chroma" else None
                )
                
                store_info = retriever.get_store_info()
                search_info[f"{store_type}_info"] = store_info
                
            except Exception as e:
                search_info[f"{store_type}_error"] = str(e)
        
        return search_info
        
    except Exception as e:
        logger.error(f"Get search info error for processing_id {processing_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get search information")

@router.get("/search/{processing_id}/similar")
async def find_similar_chunks(
    processing_id: str,
    chunk_id: str = Query(..., description="Chunk ID to find similar chunks for"),
    top_k: int = Query(5, ge=1, le=50, description="Number of similar chunks to return"),
    similarity_metric: str = Query("cosine", description="Similarity metric to use")
):
    """
    Find chunks similar to a specific chunk
    
    Given a chunk ID from previous processing, find other chunks that are similar to it.
    
    Args:
        processing_id: Processing session ID
        chunk_id: ID of the chunk to find similar chunks for
        top_k: Number of similar chunks to return
        similarity_metric: Similarity metric to use
        
    Returns:
        Similar chunks with similarity scores
    """
    try:
        # This would require storing chunk embeddings and implementing chunk-to-chunk similarity
        # For now, return a placeholder response
        
        logger.info(f"Similar chunks request: processing_id={processing_id}, chunk_id={chunk_id}")
        
        return {
            "success": False,
            "message": "Chunk-to-chunk similarity search is not implemented yet",
            "processing_id": processing_id,
            "chunk_id": chunk_id,
            "suggestion": "Use text-based search with /search/{processing_id} endpoint instead"
        }
        
    except Exception as e:
        logger.error(f"Similar chunks error: {e}")
        raise HTTPException(status_code=500, detail="Failed to find similar chunks")

@router.get("/search/models")
async def get_available_models():
    """
    Get available embedding models
    
    Returns information about available embedding models for search.
    
    Returns:
        Available models with descriptions and capabilities
    """
    try:
        from ...core.embedding import EmbeddingModelManager
        
        models_info = {}
        for model_name, model_info in EmbeddingModelManager.AVAILABLE_MODELS.items():
            models_info[model_name] = {
                "name": model_info["name"],
                "description": model_info["description"],
                "dimension": model_info["dimension"],
                "is_fallback": model_info.get("fallback", False)
            }
        
        return {
            "available_models": models_info,
            "default_model": EmbeddingModelManager.get_fallback_model(),
            "total_models": len(models_info)
        }
        
    except Exception as e:
        logger.error(f"Get models error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get available models")
