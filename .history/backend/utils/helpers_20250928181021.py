"""
Helper utilities for CSV Chunking Optimizer Pro.
"""

import uuid
import os
import json
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import pandas as pd

def generate_processing_id() -> str:
    """Generate a unique processing ID"""
    return str(uuid.uuid4())

def generate_file_id(processing_id: str, file_type: str) -> str:
    """
    Generate a unique file ID for downloads
    
    Args:
        processing_id: The processing session ID
        file_type: Type of file (chunks, embeddings, metadata, summary)
        
    Returns:
        Unique file identifier
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{file_type}_{processing_id}_{timestamp}"

def create_download_links(processing_id: str, 
                         base_url: str = "/api/v1/download",
                         expires_hours: int = 24) -> Dict[str, Dict[str, str]]:
    """
    Create download links for processed files
    
    Args:
        processing_id: The processing session ID
        base_url: Base URL for download endpoint
        expires_hours: Hours until links expire
        
    Returns:
        Dictionary of download links with metadata
    """
    expires_at = datetime.now() + timedelta(hours=expires_hours)
    expires_str = expires_at.isoformat()
    
    file_types = ['chunks', 'embeddings', 'metadata', 'summary']
    links = {}
    
    for file_type in file_types:
        file_id = generate_file_id(processing_id, file_type)
        extension = 'csv' if file_type == 'chunks' else 'json'
        
        links[f"{file_type}_{extension}"] = {
            "url": f"{base_url}/{file_id}.{extension}",
            "file_id": file_id,
            "expires_at": expires_str,
            "type": file_type
        }
    
    return links

def calculate_file_hash(file_path: str) -> str:
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception:
        return ""

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def create_processing_summary(processing_id: str,
                            layer_mode: str,
                            original_df: pd.DataFrame,
                            chunks: List[pd.DataFrame],
                            embedding_result: Any,
                            processing_time: float) -> Dict[str, Any]:
    """
    Create a comprehensive processing summary
    
    Args:
        processing_id: Unique processing identifier
        layer_mode: Processing layer mode used
        original_df: Original DataFrame
        chunks: Generated chunks
        embedding_result: Embedding generation result
        processing_time: Total processing time in seconds
        
    Returns:
        Processing summary dictionary
    """
    return {
        "processing_id": processing_id,
        "timestamp": datetime.now().isoformat(),
        "layer_mode": layer_mode,
        "processing_time_seconds": round(processing_time, 2),
        "input_data": {
            "total_rows": len(original_df),
            "total_columns": len(original_df.columns),
            "column_names": original_df.columns.tolist(),
            "data_types": original_df.dtypes.astype(str).to_dict(),
            "memory_usage_mb": round(original_df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
        },
        "chunking_results": {
            "total_chunks": len(chunks),
            "chunk_sizes": [len(chunk) for chunk in chunks],
            "average_chunk_size": round(sum(len(chunk) for chunk in chunks) / len(chunks), 2) if chunks else 0,
            "total_rows_chunked": sum(len(chunk) for chunk in chunks)
        },
        "embedding_results": {
            "model_used": getattr(embedding_result, 'model_used', 'unknown'),
            "vector_dimension": getattr(embedding_result, 'vector_dimension', 0),
            "total_embeddings": getattr(embedding_result, 'total_chunks', 0),
            "embedding_time_seconds": getattr(embedding_result, 'processing_time', 0),
            "quality_report": getattr(embedding_result, 'quality_report', {})
        },
        "performance_metrics": {
            "rows_per_second": round(len(original_df) / processing_time, 2) if processing_time > 0 else 0,
            "chunks_per_second": round(len(chunks) / processing_time, 2) if processing_time > 0 else 0,
            "embeddings_per_second": round(getattr(embedding_result, 'total_chunks', 0) / processing_time, 2) if processing_time > 0 else 0
        }
    }

def sanitize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitize DataFrame column names for safe processing
    
    Args:
        df: Input DataFrame
        
    Returns:
        DataFrame with sanitized column names
    """
    df = df.copy()
    
    # Replace problematic characters
    new_columns = []
    for col in df.columns:
        # Convert to string and strip whitespace
        clean_col = str(col).strip()
        
        # Replace spaces and special characters with underscores
        clean_col = clean_col.replace(' ', '_')
        clean_col = ''.join(c if c.isalnum() or c == '_' else '_' for c in clean_col)
        
        # Ensure it doesn't start with a number
        if clean_col and clean_col[0].isdigit():
            clean_col = f"col_{clean_col}"
        
        # Ensure it's not empty
        if not clean_col:
            clean_col = f"column_{len(new_columns)}"
        
        # Ensure uniqueness
        original_clean = clean_col
        counter = 1
        while clean_col in new_columns:
            clean_col = f"{original_clean}_{counter}"
            counter += 1
        
        new_columns.append(clean_col)
    
    df.columns = new_columns
    return df

def validate_and_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate and clean DataFrame for processing
    
    Args:
        df: Input DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    # Sanitize column names
    df = sanitize_column_names(df)
    
    # Remove completely empty rows
    df = df.dropna(how='all')
    
    # Remove completely empty columns
    df = df.dropna(axis=1, how='all')
    
    # Reset index
    df = df.reset_index(drop=True)
    
    return df

def create_error_response(error_message: str, 
                         processing_id: Optional[str] = None,
                         error_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Create standardized error response
    
    Args:
        error_message: Error description
        processing_id: Optional processing ID
        error_code: Optional error code
        
    Returns:
        Error response dictionary
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
    
    return response

def create_success_response(processing_id: str,
                          processing_summary: Dict[str, Any],
                          download_links: Dict[str, Dict[str, str]],
                          search_endpoint: Optional[str] = None) -> Dict[str, Any]:
    """
    Create standardized success response
    
    Args:
        processing_id: Processing session ID
        processing_summary: Summary of processing results
        download_links: Download links for generated files
        search_endpoint: Optional search endpoint URL
        
    Returns:
        Success response dictionary
    """
    response = {
        "success": True,
        "processing_id": processing_id,
        "timestamp": datetime.now().isoformat(),
        "processing_summary": processing_summary,
        "download_links": download_links
    }
    
    if search_endpoint:
        response["search_endpoint"] = search_endpoint
    
    return response

def get_layer_defaults(layer_mode: str) -> Dict[str, Any]:
    """
    Get default settings for different layer modes
    
    Args:
        layer_mode: Layer mode ('fast', 'config', 'deep')
        
    Returns:
        Default settings dictionary
    """
    from ..config.settings import Settings
    settings = Settings()
    
    if layer_mode == 'fast':
        return settings.LAYER_1_DEFAULTS
    elif layer_mode == 'config':
        return settings.LAYER_2_DEFAULTS
    else:  # deep
        return settings.LAYER_3_DEFAULTS

def merge_settings(base_settings: Dict[str, Any], 
                  override_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge override settings into base settings
    
    Args:
        base_settings: Base settings dictionary
        override_settings: Settings to override
        
    Returns:
        Merged settings dictionary
    """
    merged = base_settings.copy()
    
    for key, value in override_settings.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            merged[key] = merge_settings(merged[key], value)
        else:
            # Override the value
            merged[key] = value
    
    return merged
