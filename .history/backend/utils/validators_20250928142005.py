"""
Validation utilities for CSV Chunking Optimizer Pro.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Union
import base64
import io
import re

def validate_csv_data(csv_data: Union[str, bytes, pd.DataFrame]) -> pd.DataFrame:
    """
    Validate and convert CSV data to DataFrame
    
    Args:
        csv_data: CSV data as base64 string, bytes, or DataFrame
        
    Returns:
        Validated pandas DataFrame
        
    Raises:
        ValueError: If CSV data is invalid
    """
    if isinstance(csv_data, pd.DataFrame):
        if csv_data.empty:
            raise ValueError("DataFrame cannot be empty")
        return csv_data
    
    # Handle base64 encoded CSV
    if isinstance(csv_data, str):
        try:
            # Try to decode as base64
            decoded_data = base64.b64decode(csv_data)
            csv_string = decoded_data.decode('utf-8')
        except Exception:
            # Assume it's already a CSV string
            csv_string = csv_data
    elif isinstance(csv_data, bytes):
        csv_string = csv_data.decode('utf-8')
    else:
        raise ValueError("CSV data must be string, bytes, or DataFrame")
    
    # Parse CSV
    try:
        df = pd.read_csv(io.StringIO(csv_string))
        if df.empty:
            raise ValueError("CSV file is empty")
        return df
    except Exception as e:
        raise ValueError(f"Failed to parse CSV data: {str(e)}")

def validate_processing_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate processing settings
    
    Args:
        settings: Dictionary of processing settings
        
    Returns:
        Validated settings dictionary
        
    Raises:
        ValueError: If settings are invalid
    """
    validated = {}
    
    # Validate layer mode
    if 'layer_mode' in settings:
        layer_mode = settings['layer_mode']
        if layer_mode not in ['fast', 'config', 'deep']:
            raise ValueError("layer_mode must be 'fast', 'config', or 'deep'")
        validated['layer_mode'] = layer_mode
    
    # Validate preprocessing settings
    if 'preprocessing' in settings:
        preprocessing = settings['preprocessing']
        if not isinstance(preprocessing, dict):
            raise ValueError("preprocessing must be a dictionary")
        
        validated_preprocessing = {}
        
        # Validate type conversions
        if 'type_conversions' in preprocessing:
            type_conv = preprocessing['type_conversions']
            if not isinstance(type_conv, dict):
                raise ValueError("type_conversions must be a dictionary")
            
            valid_types = ['numeric', 'datetime', 'text', 'bool']
            for col, dtype in type_conv.items():
                if dtype not in valid_types:
                    raise ValueError(f"Invalid type conversion: {dtype}. Must be one of {valid_types}")
            
            validated_preprocessing['type_conversions'] = type_conv
        
        # Validate null handling
        if 'null_handling' in preprocessing:
            null_handling = preprocessing['null_handling']
            if not isinstance(null_handling, dict):
                raise ValueError("null_handling must be a dictionary")
            
            valid_strategies = ['skip', 'drop', 'mean', 'median', 'mode', 'custom']
            for col, strategy in null_handling.items():
                if isinstance(strategy, dict):
                    if 'strategy' not in strategy:
                        raise ValueError("null_handling strategy dict must have 'strategy' key")
                    if strategy['strategy'] not in valid_strategies:
                        raise ValueError(f"Invalid null handling strategy: {strategy['strategy']}")
                elif strategy not in valid_strategies:
                    raise ValueError(f"Invalid null handling strategy: {strategy}")
            
            validated_preprocessing['null_handling'] = null_handling
        
        # Validate boolean flags
        for flag in ['remove_duplicates', 'remove_stopwords']:
            if flag in preprocessing:
                if not isinstance(preprocessing[flag], bool):
                    raise ValueError(f"{flag} must be a boolean")
                validated_preprocessing[flag] = preprocessing[flag]
        
        # Validate text processing
        if 'text_processing' in preprocessing:
            text_proc = preprocessing['text_processing']
            if text_proc not in ['skip', 'lemmatize', 'stem']:
                raise ValueError("text_processing must be 'skip', 'lemmatize', or 'stem'")
            validated_preprocessing['text_processing'] = text_proc
        
        validated['preprocessing'] = validated_preprocessing
    
    # Validate chunking settings
    if 'chunking' in settings:
        chunking = settings['chunking']
        if not isinstance(chunking, dict):
            raise ValueError("chunking must be a dictionary")
        
        validated_chunking = {}
        
        # Validate chunking method
        if 'method' in chunking:
            method = chunking['method']
            valid_methods = ['fixed', 'recursive', 'document_based', 'semantic']
            if method not in valid_methods:
                raise ValueError(f"Invalid chunking method: {method}. Must be one of {valid_methods}")
            validated_chunking['method'] = method
        
        # Validate parameters based on method
        if 'chunk_size' in chunking:
            chunk_size = chunking['chunk_size']
            if not isinstance(chunk_size, int) or chunk_size <= 0:
                raise ValueError("chunk_size must be a positive integer")
            validated_chunking['chunk_size'] = chunk_size
        
        if 'overlap' in chunking:
            overlap = chunking['overlap']
            if not isinstance(overlap, int) or overlap < 0:
                raise ValueError("overlap must be a non-negative integer")
            validated_chunking['overlap'] = overlap
        
        if 'n_clusters' in chunking:
            n_clusters = chunking['n_clusters']
            if not isinstance(n_clusters, int) or n_clusters <= 0:
                raise ValueError("n_clusters must be a positive integer")
            validated_chunking['n_clusters'] = n_clusters
        
        if 'token_limit' in chunking:
            token_limit = chunking['token_limit']
            if not isinstance(token_limit, int) or token_limit <= 0:
                raise ValueError("token_limit must be a positive integer")
            validated_chunking['token_limit'] = token_limit
        
        # Copy other chunking parameters
        for key in ['key_column', 'model_name', 'preserve_headers']:
            if key in chunking:
                validated_chunking[key] = chunking[key]
        
        validated['chunking'] = validated_chunking
    
    # Validate embedding settings
    if 'embedding' in settings:
        embedding = settings['embedding']
        if not isinstance(embedding, dict):
            raise ValueError("embedding must be a dictionary")
        
        validated_embedding = {}
        
        # Validate model
        if 'model' in embedding:
            model = embedding['model']
            valid_models = ['all-MiniLM-L6-v2', 'BAAI/bge-small-en-v1.5']
            if model not in valid_models:
                raise ValueError(f"Invalid embedding model: {model}. Must be one of {valid_models}")
            validated_embedding['model'] = model
        
        # Validate batch size
        if 'batch_size' in embedding:
            batch_size = embedding['batch_size']
            if not isinstance(batch_size, int) or batch_size <= 0:
                raise ValueError("batch_size must be a positive integer")
            if batch_size > 256:
                raise ValueError("batch_size cannot exceed 256")
            validated_embedding['batch_size'] = batch_size
        
        validated['embedding'] = validated_embedding
    
    # Validate storage settings
    if 'storage' in settings:
        storage = settings['storage']
        if not isinstance(storage, dict):
            raise ValueError("storage must be a dictionary")
        
        validated_storage = {}
        
        # Validate storage type
        if 'type' in storage:
            storage_type = storage['type']
            if storage_type not in ['chroma', 'faiss']:
                raise ValueError("storage type must be 'chroma' or 'faiss'")
            validated_storage['type'] = storage_type
        
        # Validate similarity metric
        if 'similarity_metric' in storage:
            similarity = storage['similarity_metric']
            if similarity not in ['cosine', 'dot', 'euclidean']:
                raise ValueError("similarity_metric must be 'cosine', 'dot', or 'euclidean'")
            validated_storage['similarity_metric'] = similarity
        
        # Copy other storage parameters
        for key in ['persist_directory', 'collection_name']:
            if key in storage:
                validated_storage[key] = storage[key]
        
        validated['storage'] = validated_storage
    
    # Copy other top-level settings
    for key in ['filename', 'source_file']:
        if key in settings:
            validated[key] = settings[key]
    
    return validated

def validate_filename(filename: str) -> str:
    """
    Validate and sanitize filename
    
    Args:
        filename: Input filename
        
    Returns:
        Sanitized filename
        
    Raises:
        ValueError: If filename is invalid
    """
    if not filename or not isinstance(filename, str):
        raise ValueError("Filename must be a non-empty string")
    
    # Remove path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Check extension
    if not filename.lower().endswith('.csv'):
        raise ValueError("File must have .csv extension")
    
    # Sanitize filename
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    if len(filename) > 255:
        raise ValueError("Filename too long")
    
    return filename

def validate_search_parameters(query: str, 
                             model_name: str, 
                             top_k: int, 
                             similarity_metric: str) -> Dict[str, Any]:
    """
    Validate search parameters
    
    Args:
        query: Search query string
        model_name: Embedding model name
        top_k: Number of results to return
        similarity_metric: Similarity calculation method
        
    Returns:
        Validated parameters dictionary
        
    Raises:
        ValueError: If parameters are invalid
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    
    if len(query.strip()) == 0:
        raise ValueError("Query cannot be empty or whitespace only")
    
    valid_models = ['all-MiniLM-L6-v2', 'BAAI/bge-small-en-v1.5']
    if model_name not in valid_models:
        raise ValueError(f"Invalid model: {model_name}. Must be one of {valid_models}")
    
    if not isinstance(top_k, int) or top_k <= 0:
        raise ValueError("top_k must be a positive integer")
    
    if top_k > 100:
        raise ValueError("top_k cannot exceed 100")
    
    if similarity_metric not in ['cosine', 'dot', 'euclidean']:
        raise ValueError("similarity_metric must be 'cosine', 'dot', or 'euclidean'")
    
    return {
        "query": query.strip(),
        "model_name": model_name,
        "top_k": top_k,
        "similarity_metric": similarity_metric
    }

def validate_file_size(file_data: Union[str, bytes], max_size_mb: int = 100) -> bool:
    """
    Validate file size
    
    Args:
        file_data: File data as string or bytes
        max_size_mb: Maximum size in megabytes
        
    Returns:
        True if valid, raises ValueError if too large
        
    Raises:
        ValueError: If file is too large
    """
    if isinstance(file_data, str):
        # If it's base64, decode to get actual size
        try:
            decoded = base64.b64decode(file_data)
            size_bytes = len(decoded)
        except:
            # If not base64, use string length as approximation
            size_bytes = len(file_data.encode('utf-8'))
    else:
        size_bytes = len(file_data)
    
    size_mb = size_bytes / (1024 * 1024)
    
    if size_mb > max_size_mb:
        raise ValueError(f"File size ({size_mb:.2f} MB) exceeds maximum allowed size ({max_size_mb} MB)")
    
    return True
