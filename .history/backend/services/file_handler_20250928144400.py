"""
File handling service for uploads, downloads, and temporary storage
"""

import os
import json
import csv
import zipfile
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timedelta
import pandas as pd

from config.settings import settings
from ..utils.helpers import generate_file_id, format_file_size

class FileHandler:
    """Handles file operations for the API"""
    
    def __init__(self):
        self.temp_dir = settings.TEMP_FILES_DIR
        self.downloads_dir = settings.DOWNLOADS_DIR
        
        # Ensure directories exist
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
    
    async def create_download_files(self, 
                                   processing_id: str,
                                   chunking_result,
                                   embedding_result,
                                   original_df: pd.DataFrame,
                                   processed_df: pd.DataFrame,
                                   **kwargs) -> Dict[str, Dict[str, Any]]:
        """
        Create all download files for a processing job
        
        Args:
            processing_id: Processing session ID
            chunking_result: Chunking results
            embedding_result: Embedding results
            original_df: Original DataFrame
            processed_df: Processed DataFrame
            **kwargs: Additional parameters
            
        Returns:
            Dictionary of file information
        """
        files_info = {}
        
        try:
            # 1. Create chunks CSV file
            chunks_info = await self._create_chunks_csv(processing_id, chunking_result)
            files_info["chunks_csv"] = chunks_info
            
            # 2. Create embeddings JSON file
            embeddings_info = await self._create_embeddings_json(processing_id, embedding_result)
            files_info["embeddings_json"] = embeddings_info
            
            # 3. Create metadata JSON file
            metadata_info = await self._create_metadata_json(
                processing_id, original_df, processed_df, chunking_result, embedding_result, **kwargs
            )
            files_info["metadata_json"] = metadata_info
            
            # 4. Create summary JSON file
            summary_info = await self._create_summary_json(processing_id, **kwargs)
            files_info["summary_json"] = summary_info
            
            # 5. Create ZIP file with all results (optional)
            zip_info = await self._create_results_zip(processing_id, files_info)
            files_info["results_zip"] = zip_info
            
        except Exception as e:
            # If file creation fails, create minimal response
            files_info["error"] = {
                "message": f"File creation failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        
        return files_info
    
    async def _create_chunks_csv(self, processing_id: str, chunking_result) -> Dict[str, Any]:
        """Create CSV file with all chunks"""
        file_id = generate_file_id(processing_id, "chunks")
        filename = f"{file_id}.csv"
        file_path = self.downloads_dir / filename
        
        try:
            # Combine all chunks into one DataFrame
            if chunking_result and chunking_result.chunks:
                all_chunks = []
                for i, chunk in enumerate(chunking_result.chunks):
                    chunk_with_id = chunk.copy()
                    chunk_with_id['chunk_id'] = chunking_result.metadata[i].chunk_id
                    chunk_with_id['chunk_method'] = chunking_result.metadata[i].method
                    chunk_with_id['chunk_size'] = chunking_result.metadata[i].chunk_size
                    all_chunks.append(chunk_with_id)
                
                combined_df = pd.concat(all_chunks, ignore_index=True)
                combined_df.to_csv(file_path, index=False)
            else:
                # Create empty file
                pd.DataFrame().to_csv(file_path, index=False)
            
            file_size = file_path.stat().st_size
            
            return {
                "file_id": file_id,
                "filename": filename,
                "file_path": str(file_path),
                "url": f"/api/v1/download/{file_id}.csv",
                "size_bytes": file_size,
                "size_human": format_file_size(file_size),
                "type": "chunks",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=settings.FILE_RETENTION_HOURS)).isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Failed to create chunks CSV: {str(e)}",
                "file_id": file_id
            }
    
    async def _create_embeddings_json(self, processing_id: str, embedding_result) -> Dict[str, Any]:
        """Create JSON file with embeddings"""
        file_id = generate_file_id(processing_id, "embeddings")
        filename = f"{file_id}.json"
        file_path = self.downloads_dir / filename
        
        try:
            embeddings_data = {
                "model_used": getattr(embedding_result, 'model_used', 'unknown'),
                "vector_dimension": getattr(embedding_result, 'vector_dimension', 0),
                "total_chunks": getattr(embedding_result, 'total_chunks', 0),
                "processing_time": getattr(embedding_result, 'processing_time', 0.0),
                "quality_report": getattr(embedding_result, 'quality_report', {}),
                "embeddings": []
            }
            
            if hasattr(embedding_result, 'embedded_chunks') and embedding_result.embedded_chunks:
                for chunk in embedding_result.embedded_chunks:
                    embedding_data = {
                        "id": chunk.id,
                        "embedding": chunk.embedding.tolist() if hasattr(chunk.embedding, 'tolist') else list(chunk.embedding),
                        "document": chunk.document,
                        "metadata": {
                            "chunk_id": chunk.metadata.chunk_id,
                            "source_file": chunk.metadata.source_file,
                            "chunk_number": chunk.metadata.chunk_number,
                            "embedding_model": chunk.metadata.embedding_model,
                            "vector_dimension": chunk.metadata.vector_dimension,
                            "text_length": chunk.metadata.text_length
                        }
                    }
                    embeddings_data["embeddings"].append(embedding_data)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(embeddings_data, f, indent=2, ensure_ascii=False)
            
            file_size = file_path.stat().st_size
            
            return {
                "file_id": file_id,
                "filename": filename,
                "file_path": str(file_path),
                "url": f"/api/v1/download/{file_id}.json",
                "size_bytes": file_size,
                "size_human": format_file_size(file_size),
                "type": "embeddings",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=settings.FILE_RETENTION_HOURS)).isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Failed to create embeddings JSON: {str(e)}",
                "file_id": file_id
            }
    
    async def _create_metadata_json(self, processing_id: str, original_df: pd.DataFrame, 
                                   processed_df: pd.DataFrame, chunking_result, embedding_result,
                                   **kwargs) -> Dict[str, Any]:
        """Create JSON file with processing metadata"""
        file_id = generate_file_id(processing_id, "metadata")
        filename = f"{file_id}.json"
        file_path = self.downloads_dir / filename
        
        try:
            metadata = {
                "processing_info": {
                    "processing_id": processing_id,
                    "timestamp": datetime.now().isoformat(),
                    "layer_mode": kwargs.get("layer_mode", "unknown")
                },
                "input_data": {
                    "original_rows": len(original_df),
                    "original_columns": len(original_df.columns),
                    "original_column_names": original_df.columns.tolist(),
                    "processed_rows": len(processed_df),
                    "processed_columns": len(processed_df.columns),
                    "processed_column_names": processed_df.columns.tolist(),
                    "data_types": processed_df.dtypes.astype(str).to_dict()
                },
                "chunking_info": {
                    "method": getattr(chunking_result, 'method', 'unknown'),
                    "total_chunks": getattr(chunking_result, 'total_chunks', 0),
                    "quality_report": getattr(chunking_result, 'quality_report', {})
                },
                "embedding_info": {
                    "model_used": getattr(embedding_result, 'model_used', 'unknown'),
                    "vector_dimension": getattr(embedding_result, 'vector_dimension', 0),
                    "total_embeddings": getattr(embedding_result, 'total_chunks', 0),
                    "processing_time": getattr(embedding_result, 'processing_time', 0.0),
                    "quality_report": getattr(embedding_result, 'quality_report', {})
                }
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            file_size = file_path.stat().st_size
            
            return {
                "file_id": file_id,
                "filename": filename,
                "file_path": str(file_path),
                "url": f"/api/v1/download/{file_id}.json",
                "size_bytes": file_size,
                "size_human": format_file_size(file_size),
                "type": "metadata",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=settings.FILE_RETENTION_HOURS)).isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Failed to create metadata JSON: {str(e)}",
                "file_id": file_id
            }
    
    async def _create_summary_json(self, processing_id: str, **kwargs) -> Dict[str, Any]:
        """Create JSON file with processing summary"""
        file_id = generate_file_id(processing_id, "summary")
        filename = f"{file_id}.json"
        file_path = self.downloads_dir / filename
        
        try:
            from ..utils.helpers import create_processing_summary
            
            summary = create_processing_summary(
                processing_id=processing_id,
                layer_mode=kwargs.get("layer_mode", "unknown"),
                original_df=kwargs.get("original_df"),
                chunks=kwargs.get("chunking_result", {}).chunks if kwargs.get("chunking_result") else [],
                embedding_result=kwargs.get("embedding_result"),
                processing_time=kwargs.get("processing_time", 0.0)
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            file_size = file_path.stat().st_size
            
            return {
                "file_id": file_id,
                "filename": filename,
                "file_path": str(file_path),
                "url": f"/api/v1/download/{file_id}.json",
                "size_bytes": file_size,
                "size_human": format_file_size(file_size),
                "type": "summary",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=settings.FILE_RETENTION_HOURS)).isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Failed to create summary JSON: {str(e)}",
                "file_id": file_id
            }
    
    async def _create_results_zip(self, processing_id: str, files_info: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Create ZIP file containing all results"""
        file_id = generate_file_id(processing_id, "results")
        filename = f"{file_id}.zip"
        file_path = self.downloads_dir / filename
        
        try:
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_type, file_info in files_info.items():
                    if file_type != "error" and "file_path" in file_info:
                        source_path = Path(file_info["file_path"])
                        if source_path.exists():
                            zipf.write(source_path, source_path.name)
            
            file_size = file_path.stat().st_size
            
            return {
                "file_id": file_id,
                "filename": filename,
                "file_path": str(file_path),
                "url": f"/api/v1/download/{file_id}.zip",
                "size_bytes": file_size,
                "size_human": format_file_size(file_size),
                "type": "results_zip",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=settings.FILE_RETENTION_HOURS)).isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Failed to create results ZIP: {str(e)}",
                "file_id": file_id
            }
    
    def get_file_path(self, file_id: str, extension: str = None) -> Path:
        """Get file path for a file ID"""
        if extension:
            filename = f"{file_id}.{extension}"
        else:
            # Try to find file with any extension
            for ext in ['csv', 'json', 'zip']:
                potential_file = self.downloads_dir / f"{file_id}.{ext}"
                if potential_file.exists():
                    return potential_file
            filename = file_id
        
        return self.downloads_dir / filename
    
    def cleanup_expired_files(self):
        """Clean up expired files"""
        try:
            current_time = datetime.now()
            cutoff_time = current_time - timedelta(hours=settings.FILE_RETENTION_HOURS)
            
            # Clean temp files
            for file_path in self.temp_dir.glob("*"):
                if file_path.stat().st_mtime < cutoff_time.timestamp():
                    file_path.unlink()
            
            # Clean download files
            for file_path in self.downloads_dir.glob("*"):
                if file_path.stat().st_mtime < cutoff_time.timestamp():
                    file_path.unlink()
                    
        except Exception as e:
            print(f"Cleanup failed: {e}")
