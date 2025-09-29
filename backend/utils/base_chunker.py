"""
Base classes and data structures for chunking operations.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from dataclasses import dataclass
from abc import ABC, abstractmethod
import warnings

@dataclass
class ChunkMetadata:
    """Metadata for a single chunk"""
    chunk_id: str
    start_idx: int
    end_idx: int
    chunk_size: int
    method: str
    quality_score: Optional[float] = None
    additional_metadata: Optional[Dict[str, Any]] = None

@dataclass
class ChunkingResult:
    """Result of a chunking operation"""
    chunks: List[pd.DataFrame]
    metadata: List[ChunkMetadata]
    method: str
    total_chunks: int
    quality_report: Dict[str, Any]

class ChunkingQualityAssessment:
    """Assess the quality of chunking results"""
    
    @staticmethod
    def comprehensive_assessment(chunks: List[pd.DataFrame], original_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Perform comprehensive quality assessment of chunks
        
        Args:
            chunks: List of DataFrame chunks
            original_df: Original DataFrame before chunking
            
        Returns:
            Quality assessment report
        """
        if not chunks:
            return {
                "overall_quality": "POOR",
                "coverage": 0.0,
                "total_chunks": 0,
                "error": "No chunks generated"
            }
        
        # Basic metrics
        total_rows_chunked = sum(len(chunk) for chunk in chunks)
        original_rows = len(original_df)
        coverage = total_rows_chunked / original_rows if original_rows > 0 else 0.0
        
        # Size distribution
        chunk_sizes = [len(chunk) for chunk in chunks]
        avg_chunk_size = np.mean(chunk_sizes)
        size_variance = np.var(chunk_sizes)
        size_std = np.std(chunk_sizes)
        
        # Quality checks
        empty_chunks = sum(1 for chunk in chunks if chunk.empty)
        very_small_chunks = sum(1 for size in chunk_sizes if size < 3)
        very_large_chunks = sum(1 for size in chunk_sizes if size > original_rows * 0.8)
        
        # Overall quality score
        quality_score = 1.0
        
        # Penalize poor coverage
        if coverage < 0.95:
            quality_score -= (0.95 - coverage) * 2
        
        # Penalize empty or very small chunks
        if empty_chunks > 0:
            quality_score -= empty_chunks * 0.1
        if very_small_chunks > 0:
            quality_score -= very_small_chunks * 0.05
        
        # Penalize very large chunks (poor chunking)
        if very_large_chunks > 0:
            quality_score -= very_large_chunks * 0.2
        
        # Penalize high variance in chunk sizes (inconsistent chunking)
        if size_std > avg_chunk_size * 0.5:
            quality_score -= 0.1
        
        quality_score = max(0.0, min(1.0, quality_score))
        
        # Determine quality label
        if quality_score >= 0.8:
            quality_label = "EXCELLENT"
        elif quality_score >= 0.6:
            quality_label = "GOOD"
        elif quality_score >= 0.4:
            quality_label = "FAIR"
        else:
            quality_label = "POOR"
        
        return {
            "overall_quality": quality_label,
            "quality_score": quality_score,
            "coverage": coverage,
            "total_chunks": len(chunks),
            "total_rows_processed": total_rows_chunked,
            "original_rows": original_rows,
            "chunk_size_stats": {
                "mean": avg_chunk_size,
                "std": size_std,
                "variance": size_variance,
                "min": min(chunk_sizes),
                "max": max(chunk_sizes)
            },
            "quality_issues": {
                "empty_chunks": empty_chunks,
                "very_small_chunks": very_small_chunks,
                "very_large_chunks": very_large_chunks
            }
        }

class BaseChunker(ABC):
    """Abstract base class for all chunking strategies"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def chunk(self, dataframe: pd.DataFrame, **kwargs) -> ChunkingResult:
        """
        Chunk the dataframe according to the strategy
        
        Args:
            dataframe: Input DataFrame to chunk
            **kwargs: Strategy-specific parameters
            
        Returns:
            ChunkingResult with chunks and metadata
        """
        pass
    
    def validate_input(self, dataframe: pd.DataFrame):
        """Validate input DataFrame"""
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame")
        if dataframe.empty:
            raise ValueError("DataFrame cannot be empty")
        if len(dataframe.columns) == 0:
            raise ValueError("DataFrame must have at least one column")
    
    def create_chunk_metadata(self, 
                            chunk: pd.DataFrame, 
                            chunk_index: int,
                            start_idx: int, 
                            end_idx: int,
                            original_df: pd.DataFrame,
                            extra_metadata: Dict[str, Any] = None) -> ChunkMetadata:
        """
        Create metadata for a chunk
        
        Args:
            chunk: The DataFrame chunk
            chunk_index: Index of this chunk in the sequence
            start_idx: Starting row index in original DataFrame
            end_idx: Ending row index in original DataFrame
            original_df: Original DataFrame
            extra_metadata: Additional metadata to include
            
        Returns:
            ChunkMetadata object
        """
        return ChunkMetadata(
            chunk_id=f"{self.name}_chunk_{chunk_index:04d}",
            start_idx=start_idx,
            end_idx=end_idx,
            chunk_size=len(chunk),
            method=self.name,
            additional_metadata=extra_metadata or {}
        )
    
    def assess_chunk_quality(self, chunks: List[pd.DataFrame], original_df: pd.DataFrame) -> Dict[str, Any]:
        """Assess the quality of generated chunks"""
        return ChunkingQualityAssessment.comprehensive_assessment(chunks, original_df)

# Utility functions
def validate_chunking_parameters(**kwargs) -> Dict[str, Any]:
    """Validate and normalize chunking parameters"""
    validated = {}
    
    # Common parameter validation
    if 'chunk_size' in kwargs:
        chunk_size = kwargs['chunk_size']
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer")
        validated['chunk_size'] = chunk_size
    
    if 'overlap' in kwargs:
        overlap = kwargs['overlap']
        if not isinstance(overlap, int) or overlap < 0:
            raise ValueError("overlap must be a non-negative integer")
        validated['overlap'] = overlap
    
    if 'n_clusters' in kwargs:
        n_clusters = kwargs['n_clusters']
        if not isinstance(n_clusters, int) or n_clusters <= 0:
            raise ValueError("n_clusters must be a positive integer")
        validated['n_clusters'] = n_clusters
    
    if 'token_limit' in kwargs:
        token_limit = kwargs['token_limit']
        if not isinstance(token_limit, int) or token_limit <= 0:
            raise ValueError("token_limit must be a positive integer")
        validated['token_limit'] = token_limit
    
    # Copy other parameters as-is
    for key, value in kwargs.items():
        if key not in validated:
            validated[key] = value
    
    return validated

def create_chunk_summary(chunking_result: ChunkingResult) -> Dict[str, Any]:
    """Create a summary of chunking results"""
    return {
        "method": chunking_result.method,
        "total_chunks": chunking_result.total_chunks,
        "quality_report": chunking_result.quality_report,
        "chunk_size_distribution": [len(chunk) for chunk in chunking_result.chunks],
        "metadata_summary": {
            "chunk_ids": [meta.chunk_id for meta in chunking_result.metadata],
            "size_range": {
                "min": min(meta.chunk_size for meta in chunking_result.metadata),
                "max": max(meta.chunk_size for meta in chunking_result.metadata)
            }
        }
    }
