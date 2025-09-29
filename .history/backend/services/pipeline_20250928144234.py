"""
Processing pipeline orchestrator - coordinates all backend modules
"""

import asyncio
import time
from typing import Dict, Any, List, Tuple
import pandas as pd
from datetime import datetime

from ..core.preprocessing import preprocess_csv
from ..core.chunking import chunk_dataframe
from ..core.embedding import generate_chunk_embeddings
from ..core.storing import store_embeddings
from ..core.retrieval import create_retriever
from ..utils.helpers import generate_processing_id, create_processing_summary, merge_settings, get_layer_defaults
from ..utils.validators import validate_csv_data, validate_processing_settings

class ProcessingPipeline:
    """Main processing pipeline orchestrator"""
    
    def __init__(self):
        self.active_jobs = {}  # In-memory job tracking
    
    async def process_csv(self, 
                         csv_data: str, 
                         filename: str,
                         layer_mode: str = "fast",
                         custom_settings: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Main processing pipeline
        
        Args:
            csv_data: Base64 encoded CSV data
            filename: Original filename
            layer_mode: Processing layer mode
            custom_settings: Custom processing settings
            
        Returns:
            Processing results with download links
        """
        processing_id = generate_processing_id()
        start_time = time.time()
        
        try:
            # Step 1: Validate and prepare data
            df = validate_csv_data(csv_data)
            
            # Step 2: Merge settings
            base_settings = get_layer_defaults(layer_mode)
            if custom_settings:
                settings = merge_settings(base_settings, custom_settings)
            else:
                settings = base_settings
            
            # Validate settings
            validated_settings = validate_processing_settings(settings)
            
            # Step 3: Preprocessing
            preprocessing_result = await self._run_preprocessing(df, validated_settings.get("preprocessing", {}))
            processed_df, file_meta, numeric_meta = preprocessing_result
            
            # Step 4: Chunking
            chunking_result = await self._run_chunking(processed_df, validated_settings.get("chunking", {}))
            
            # Step 5: Embedding
            embedding_result = await self._run_embedding(
                chunking_result, 
                validated_settings.get("embedding", {}),
                filename
            )
            
            # Step 6: Storage
            storage_result = await self._run_storage(
                embedding_result,
                validated_settings.get("storage", {})
            )
            
            # Step 7: Create files and response
            processing_time = time.time() - start_time
            
            response = await self._create_response(
                processing_id=processing_id,
                layer_mode=layer_mode,
                original_df=df,
                processed_df=processed_df,
                chunking_result=chunking_result,
                embedding_result=embedding_result,
                storage_result=storage_result,
                processing_time=processing_time,
                filename=filename
            )
            
            return response
            
        except Exception as e:
            # Handle errors
            error_response = {
                "success": False,
                "processing_id": processing_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "processing_time_seconds": time.time() - start_time
            }
            return error_response
    
    async def _run_preprocessing(self, df: pd.DataFrame, settings: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any], List[Dict[str, Any]]]:
        """Run preprocessing step"""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                preprocess_csv,
                df,
                settings
            )
            return result
        except Exception as e:
            # Fallback to basic preprocessing
            return df, {}, []
    
    async def _run_chunking(self, df: pd.DataFrame, settings: Dict[str, Any]):
        """Run chunking step"""
        method = settings.get("method", "fixed")
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                chunk_dataframe,
                df,
                method,
                settings
            )
            return result
        except Exception as e:
            # Fallback to fixed chunking
            from ..core.chunking import chunk_fixed
            return await loop.run_in_executor(None, chunk_fixed, df, 100, 0)
    
    async def _run_embedding(self, chunking_result, settings: Dict[str, Any], source_file: str):
        """Run embedding step"""
        model_name = settings.get("model", "all-MiniLM-L6-v2")
        batch_size = settings.get("batch_size", 32)
        
        # Prepare metadata
        chunk_metadata = []
        for i, metadata in enumerate(chunking_result.metadata):
            chunk_meta = {
                "chunk_id": metadata.chunk_id,
                "method": metadata.method,
                "chunk_size": metadata.chunk_size,
                "start_idx": metadata.start_idx,
                "end_idx": metadata.end_idx
            }
            if metadata.additional_metadata:
                chunk_meta.update(metadata.additional_metadata)
            chunk_metadata.append(chunk_meta)
        
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                generate_chunk_embeddings,
                chunking_result.chunks,
                chunk_metadata,
                model_name,
                batch_size,
                source_file
            )
            return result
        except Exception as e:
            # Create dummy result
            from ..core.embedding import EmbeddingResult
            return EmbeddingResult(
                embedded_chunks=[],
                model_used="dummy",
                total_chunks=0,
                vector_dimension=384,
                quality_report={"error": str(e)},
                processing_time=0.0
            )
    
    async def _run_storage(self, embedding_result, settings: Dict[str, Any]):
        """Run storage step"""
        store_type = settings.get("type", "chroma")
        
        try:
            if not embedding_result.embedded_chunks:
                return {"store_type": store_type, "stored_count": 0}
            
            loop = asyncio.get_event_loop()
            store = await loop.run_in_executor(
                None,
                store_embeddings,
                embedding_result.embedded_chunks,
                store_type,
                f"./backend/storage/.{store_type}",
                "csv_chunks" if store_type == "chroma" else None,
                embedding_result.vector_dimension if store_type == "faiss" else None
            )
            
            return {
                "store_type": store_type,
                "stored_count": len(embedding_result.embedded_chunks),
                "store": store
            }
            
        except Exception as e:
            return {
                "store_type": store_type,
                "stored_count": 0,
                "error": str(e)
            }
    
    async def _create_response(self, **kwargs) -> Dict[str, Any]:
        """Create final response with download links"""
        from .file_handler import FileHandler
        from .response_builder import ResponseBuilder
        
        file_handler = FileHandler()
        response_builder = ResponseBuilder()
        
        # Generate files
        files_info = await file_handler.create_download_files(**kwargs)
        
        # Build response
        response = response_builder.build_success_response(
            files_info=files_info,
            **kwargs
        )
        
        return response
    
    async def search_chunks(self, 
                           processing_id: str,
                           query: str,
                           model_name: str = "all-MiniLM-L6-v2",
                           top_k: int = 5,
                           similarity_metric: str = "cosine",
                           store_type: str = "chroma") -> Dict[str, Any]:
        """
        Search processed chunks
        
        Args:
            processing_id: Processing session ID
            query: Search query
            model_name: Embedding model
            top_k: Number of results
            similarity_metric: Similarity metric
            store_type: Vector store type
            
        Returns:
            Search results
        """
        start_time = time.time()
        
        try:
            # Create retriever
            retriever = create_retriever(
                store_type=store_type,
                persist_directory=f"./backend/storage/.{store_type}",
                collection_name="csv_chunks" if store_type == "chroma" else None
            )
            
            # Perform search
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None,
                retriever.search,
                query,
                model_name,
                top_k,
                similarity_metric
            )
            
            # Format response
            formatted_results = []
            if results.get("documents") and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    result_item = {
                        "chunk_id": results["ids"][0][i] if results.get("ids") else f"chunk_{i}",
                        "document": doc,
                        "similarity_score": results["distances"][0][i] if results.get("distances") else 0.0,
                        "metadata": results["metadatas"][0][i] if results.get("metadatas") else {}
                    }
                    formatted_results.append(result_item)
            
            return {
                "success": True,
                "processing_id": processing_id,
                "query": query,
                "similarity_metric": similarity_metric,
                "total_results": len(formatted_results),
                "results": formatted_results,
                "processing_time_seconds": time.time() - start_time
            }
            
        except Exception as e:
            return {
                "success": False,
                "processing_id": processing_id,
                "query": query,
                "error": str(e),
                "processing_time_seconds": time.time() - start_time
            }
