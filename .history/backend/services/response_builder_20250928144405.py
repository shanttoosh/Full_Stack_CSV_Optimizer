"""
Response builder service for standardized API responses
"""

from typing import Dict, Any, List
from datetime import datetime
from ..utils.helpers import create_success_response, create_error_response

class ResponseBuilder:
    """Builds standardized API responses"""
    
    def build_success_response(self, 
                              processing_id: str,
                              layer_mode: str,
                              files_info: Dict[str, Dict[str, Any]],
                              processing_time: float,
                              **kwargs) -> Dict[str, Any]:
        """
        Build success response for processing
        
        Args:
            processing_id: Processing session ID
            layer_mode: Layer mode used
            files_info: Information about generated files
            processing_time: Total processing time
            **kwargs: Additional response data
            
        Returns:
            Standardized success response
        """
        
        # Create processing summary
        processing_summary = self._create_processing_summary(
            processing_id=processing_id,
            layer_mode=layer_mode,
            processing_time=processing_time,
            **kwargs
        )
        
        # Create download links
        download_links = self._create_download_links(files_info)
        
        # Build response
        response = {
            "success": True,
            "processing_id": processing_id,
            "timestamp": datetime.now().isoformat(),
            "processing_summary": processing_summary,
            "download_links": download_links,
            "search_endpoint": f"/api/v1/search/{processing_id}",
            "message": "Processing completed successfully"
        }
        
        return response
    
    def build_error_response(self, 
                           error_message: str,
                           processing_id: str = None,
                           error_code: str = None,
                           **kwargs) -> Dict[str, Any]:
        """
        Build error response
        
        Args:
            error_message: Error description
            processing_id: Optional processing ID
            error_code: Optional error code
            **kwargs: Additional error data
            
        Returns:
            Standardized error response
        """
        
        response = {
            "success": False,
            "error": error_message,
            "timestamp": datetime.now().isoformat()
        }
        
        if processing_id:
            response["processing_id"] = processing_id
        
        if error_code:
            response["error_code"] = error_code
        
        # Add additional error data
        for key, value in kwargs.items():
            if key not in response:
                response[key] = value
        
        return response
    
    def build_search_response(self,
                            processing_id: str,
                            query: str,
                            results: List[Dict[str, Any]],
                            similarity_metric: str,
                            processing_time: float,
                            **kwargs) -> Dict[str, Any]:
        """
        Build search response
        
        Args:
            processing_id: Processing session ID
            query: Search query
            results: Search results
            similarity_metric: Similarity metric used
            processing_time: Search processing time
            **kwargs: Additional search data
            
        Returns:
            Standardized search response
        """
        
        response = {
            "success": True,
            "processing_id": processing_id,
            "query": query,
            "similarity_metric": similarity_metric,
            "total_results": len(results),
            "results": results,
            "processing_time_seconds": processing_time,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add additional search data
        for key, value in kwargs.items():
            if key not in response:
                response[key] = value
        
        return response
    
    def build_health_response(self) -> Dict[str, Any]:
        """Build health check response"""
        
        # Check service availability
        services = self._check_services()
        
        # Determine overall status
        overall_status = "healthy" if all(status == "healthy" for status in services.values()) else "degraded"
        
        response = {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "services": services
        }
        
        return response
    
    def build_info_response(self) -> Dict[str, Any]:
        """Build API information response"""
        
        response = {
            "app_name": "CSV Chunking Optimizer Pro API",
            "version": "1.0.0",
            "description": "Complete CSV processing, chunking, embedding, and retrieval API",
            "available_endpoints": [
                "POST /api/v1/layer1/process",
                "POST /api/v1/layer2/process", 
                "POST /api/v1/layer3/process",
                "POST /api/v1/process-csv",
                "POST /api/v1/search/{processing_id}",
                "GET /api/v1/download/{file_id}",
                "GET /api/v1/health",
                "GET /api/v1/info"
            ],
            "supported_models": [
                "all-MiniLM-L6-v2",
                "BAAI/bge-small-en-v1.5"
            ],
            "supported_chunking_methods": [
                "fixed",
                "recursive", 
                "document_based",
                "semantic"
            ],
            "supported_similarity_metrics": [
                "cosine",
                "dot",
                "euclidean"
            ],
            "supported_storage_types": [
                "chroma",
                "faiss"
            ],
            "max_file_size_mb": 100,
            "file_retention_hours": 24
        }
        
        return response
    
    def _create_processing_summary(self, 
                                 processing_id: str,
                                 layer_mode: str,
                                 processing_time: float,
                                 **kwargs) -> Dict[str, Any]:
        """Create processing summary"""
        
        summary = {
            "processing_id": processing_id,
            "layer_mode": layer_mode,
            "timestamp": datetime.now().isoformat(),
            "processing_time_seconds": round(processing_time, 2)
        }
        
        # Add input data info
        if "original_df" in kwargs:
            df = kwargs["original_df"]
            summary["input_data"] = {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "data_types": df.dtypes.astype(str).to_dict()
            }
        
        # Add chunking info
        if "chunking_result" in kwargs:
            chunking_result = kwargs["chunking_result"]
            summary["chunking_results"] = {
                "method": getattr(chunking_result, 'method', 'unknown'),
                "total_chunks": getattr(chunking_result, 'total_chunks', 0),
                "quality_report": getattr(chunking_result, 'quality_report', {})
            }
        
        # Add embedding info
        if "embedding_result" in kwargs:
            embedding_result = kwargs["embedding_result"]
            summary["embedding_results"] = {
                "model_used": getattr(embedding_result, 'model_used', 'unknown'),
                "vector_dimension": getattr(embedding_result, 'vector_dimension', 0),
                "total_embeddings": getattr(embedding_result, 'total_chunks', 0),
                "processing_time": getattr(embedding_result, 'processing_time', 0.0),
                "quality_report": getattr(embedding_result, 'quality_report', {})
            }
        
        # Add performance metrics
        if processing_time > 0:
            input_rows = summary.get("input_data", {}).get("total_rows", 0)
            total_chunks = summary.get("chunking_results", {}).get("total_chunks", 0)
            
            summary["performance_metrics"] = {
                "rows_per_second": round(input_rows / processing_time, 2) if input_rows else 0,
                "chunks_per_second": round(total_chunks / processing_time, 2) if total_chunks else 0
            }
        
        return summary
    
    def _create_download_links(self, files_info: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Create download links from files info"""
        
        download_links = {}
        
        for file_type, file_info in files_info.items():
            if "error" not in file_info and "url" in file_info:
                download_links[file_type] = {
                    "url": file_info["url"],
                    "file_id": file_info.get("file_id", ""),
                    "size_bytes": file_info.get("size_bytes", 0),
                    "size_human": file_info.get("size_human", "0 B"),
                    "type": file_info.get("type", file_type),
                    "expires_at": file_info.get("expires_at", ""),
                    "created_at": file_info.get("created_at", "")
                }
        
        return download_links
    
    def _check_services(self) -> Dict[str, str]:
        """Check service availability"""
        
        services = {}
        
        # Check core modules
        try:
            from ..core import preprocessing, chunking, embedding, storing, retrieval
            services["core_modules"] = "healthy"
        except Exception:
            services["core_modules"] = "unhealthy"
        
        # Check storage availability
        try:
            from ..core.storing import get_available_stores
            available_stores = get_available_stores()
            services["vector_stores"] = "healthy" if available_stores else "degraded"
        except Exception:
            services["vector_stores"] = "unhealthy"
        
        # Check embedding models
        try:
            import sentence_transformers
            services["embedding_models"] = "healthy"
        except Exception:
            services["embedding_models"] = "degraded"
        
        # Check file system
        try:
            from config.settings import settings
            settings.DOWNLOADS_DIR.mkdir(exist_ok=True)
            services["file_system"] = "healthy"
        except Exception:
            services["file_system"] = "unhealthy"
        
        return services
