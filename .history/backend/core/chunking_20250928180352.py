"""
Complete unified chunking module for CSV Chunking Optimizer Pro.
Supports: Fixed Size, Recursive, Document-based, and Semantic chunking.
"""

from typing import List, Dict, Any, Optional, Union, Tuple
import pandas as pd
import numpy as np
import warnings
from abc import ABC, abstractmethod

# Import base classes from utils
from ..utils.base_chunker import BaseChunker, ChunkingResult, ChunkMetadata, validate_chunking_parameters

# Import dependencies with fallbacks
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    warnings.warn("langchain not available, recursive chunking will use fallback implementation")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    warnings.warn("sentence-transformers not available, semantic chunking will be limited")

try:
    from sklearn.cluster import KMeans
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    warnings.warn("scikit-learn not available, semantic chunking will be limited")

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    warnings.warn("tiktoken not available, token counting will use character approximation")

class FixedSizeChunker(BaseChunker):
    """Fixed size chunking - splits DataFrame into fixed-size chunks with optional overlap"""
    
    def __init__(self):
        super().__init__("fixed_size")
    
    def chunk(self, dataframe: pd.DataFrame, chunk_size: int = 100, overlap: int = 0, **kwargs) -> ChunkingResult:
        """
        Chunk dataframe into fixed-size chunks
        
        Args:
            dataframe: Input DataFrame
            chunk_size: Number of rows per chunk
            overlap: Number of overlapping rows between chunks
            
        Returns:
            ChunkingResult with fixed-size chunks
        """
        self.validate_input(dataframe)
        
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if overlap < 0:
            raise ValueError("overlap cannot be negative")
        if overlap >= chunk_size:
            raise ValueError("overlap must be less than chunk_size")
        
        chunks = []
        metadata_list = []
        
        total_rows = len(dataframe)
        step = max(1, chunk_size - overlap)
        
        chunk_index = 0
        for start_idx in range(0, total_rows, step):
            end_idx = min(start_idx + chunk_size, total_rows)
            
            chunk_df = dataframe.iloc[start_idx:end_idx].copy()
            chunks.append(chunk_df)
            
            metadata = self.create_chunk_metadata(
                chunk=chunk_df,
                chunk_index=chunk_index,
                start_idx=start_idx,
                end_idx=end_idx - 1,
                original_df=dataframe,
                extra_metadata={
                    'chunk_size_param': chunk_size,
                    'overlap': overlap,
                    'actual_size': len(chunk_df),
                    'chunking_method': 'fixed_size'
                }
            )
            metadata_list.append(metadata)
            chunk_index += 1
            
            if end_idx >= total_rows:
                break
        
        quality_report = self.assess_chunk_quality(chunks, dataframe)
        
        return ChunkingResult(
            chunks=chunks,
            metadata=metadata_list,
            method=self.name,
            total_chunks=len(chunks),
            quality_report=quality_report
        )

class RecursiveChunker(BaseChunker):
    """Recursive text splitting chunker - converts DataFrame to text and splits recursively"""
    
    def __init__(self):
        super().__init__("recursive")
    
    def chunk(self, dataframe: pd.DataFrame, chunk_size: int = 400, overlap: int = 50, **kwargs) -> ChunkingResult:
        """
        Chunk dataframe using recursive text splitting
        
        Args:
            dataframe: Input DataFrame
            chunk_size: Character-based chunk size
            overlap: Character-based overlap
            
        Returns:
            ChunkingResult with recursively split chunks
        """
        self.validate_input(dataframe)
        
        if LANGCHAIN_AVAILABLE:
            return self._chunk_with_langchain(dataframe, chunk_size, overlap, **kwargs)
        else:
            return self._chunk_fallback(dataframe, chunk_size, overlap, **kwargs)
    
    def _chunk_with_langchain(self, dataframe: pd.DataFrame, chunk_size: int, overlap: int, **kwargs) -> ChunkingResult:
        """Use langchain's RecursiveCharacterTextSplitter"""
        # Convert DataFrame to text
        text_rows = []
        for _, row in dataframe.iterrows():
            kv_pairs = [f"{col}: {row[col]}" for col in dataframe.columns if pd.notna(row[col])]
            text_rows.append(" | ".join(kv_pairs))
        
        big_text = "\n".join(text_rows)
        
        # Split text using langchain
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        text_chunks = splitter.split_text(big_text)
        
        # Convert text chunks back to DataFrames (approximate)
        chunks = []
        metadata_list = []
        
        for chunk_index, text_chunk in enumerate(text_chunks):
            # Create a single-row DataFrame with the text chunk
            chunk_df = pd.DataFrame({'text': [text_chunk]})
            chunks.append(chunk_df)
            
            metadata = self.create_chunk_metadata(
                chunk=chunk_df,
                chunk_index=chunk_index,
                start_idx=0,  # Text-based, so approximate
                end_idx=0,
                original_df=dataframe,
                extra_metadata={
                    'chunk_size_param': chunk_size,
                    'overlap': overlap,
                    'text_length': len(text_chunk),
                    'chunking_method': 'recursive_langchain'
                }
            )
            metadata_list.append(metadata)
        
        quality_report = self.assess_chunk_quality(chunks, dataframe)
        
        return ChunkingResult(
            chunks=chunks,
            metadata=metadata_list,
            method=self.name,
            total_chunks=len(chunks),
            quality_report=quality_report
        )
    
    def _chunk_fallback(self, dataframe: pd.DataFrame, chunk_size: int, overlap: int, **kwargs) -> ChunkingResult:
        """Fallback implementation without langchain"""
        # Simple character-based splitting
        text_rows = []
        row_indices = []
        
        for idx, row in dataframe.iterrows():
            kv_pairs = [f"{col}: {row[col]}" for col in dataframe.columns if pd.notna(row[col])]
            text_row = " | ".join(kv_pairs)
            text_rows.append(text_row)
            row_indices.append(idx)
        
        # Simple splitting by character count
        chunks = []
        metadata_list = []
        chunk_index = 0
        
        current_chunk_text = ""
        current_chunk_rows = []
        current_char_count = 0
        
        for i, (text_row, orig_idx) in enumerate(zip(text_rows, row_indices)):
            if current_char_count + len(text_row) > chunk_size and current_chunk_rows:
                # Finish current chunk
                chunk_df = dataframe.loc[current_chunk_rows].copy()
                chunks.append(chunk_df)
                
                metadata = self.create_chunk_metadata(
                    chunk=chunk_df,
                    chunk_index=chunk_index,
                    start_idx=current_chunk_rows[0],
                    end_idx=current_chunk_rows[-1],
                    original_df=dataframe,
                    extra_metadata={
                        'chunk_size_param': chunk_size,
                        'overlap': overlap,
                        'text_length': len(current_chunk_text),
                        'chunking_method': 'recursive_fallback'
                    }
                )
                metadata_list.append(metadata)
                chunk_index += 1
                
                # Handle overlap
                overlap_rows = max(0, min(overlap // 100, len(current_chunk_rows)))  # Approximate overlap
                current_chunk_rows = current_chunk_rows[-overlap_rows:] if overlap_rows > 0 else []
                current_chunk_text = "\n".join([text_rows[row_indices.index(r)] for r in current_chunk_rows])
                current_char_count = len(current_chunk_text)
            
            current_chunk_rows.append(orig_idx)
            current_chunk_text += "\n" + text_row
            current_char_count += len(text_row) + 1
        
        # Handle last chunk
        if current_chunk_rows:
            chunk_df = dataframe.loc[current_chunk_rows].copy()
            chunks.append(chunk_df)
            
            metadata = self.create_chunk_metadata(
                chunk=chunk_df,
                chunk_index=chunk_index,
                start_idx=current_chunk_rows[0],
                end_idx=current_chunk_rows[-1],
                original_df=dataframe,
                extra_metadata={
                    'chunk_size_param': chunk_size,
                    'overlap': overlap,
                    'text_length': len(current_chunk_text),
                    'chunking_method': 'recursive_fallback'
                }
            )
            metadata_list.append(metadata)
        
        quality_report = self.assess_chunk_quality(chunks, dataframe)
        
        return ChunkingResult(
            chunks=chunks,
            metadata=metadata_list,
            method=self.name,
            total_chunks=len(chunks),
            quality_report=quality_report
        )

class DocumentBasedChunker(BaseChunker):
    """Document-based chunking - groups by key column and splits by token count"""
    
    def __init__(self):
        super().__init__("document_based")
    
    def chunk(self, dataframe: pd.DataFrame, key_column: str, 
              token_limit: int = 2000, model_name: str = "gpt-4",
              preserve_headers: bool = True, **kwargs) -> ChunkingResult:
        """
        Chunk dataframe using document-based approach
        
        Args:
            dataframe: Input DataFrame
            key_column: Column name to group rows by
            token_limit: Maximum tokens per chunk
            model_name: Model for token counting
            preserve_headers: Whether to include headers in each chunk
            
        Returns:
            ChunkingResult with document-based chunks
        """
        self.validate_input(dataframe)
        
        if key_column not in dataframe.columns:
            raise ValueError(f"Key column '{key_column}' not found in dataframe")
        
        # Initialize tokenizer if available
        tokenizer = None
        if TIKTOKEN_AVAILABLE:
            try:
                tokenizer = tiktoken.encoding_for_model(model_name)
            except Exception:
                # Fallback to cl100k_base encoding
                try:
                    tokenizer = tiktoken.get_encoding("cl100k_base")
                except:
                    tokenizer = None
        
        chunks = []
        metadata_list = []
        
        # Group by key column
        grouped = dataframe.groupby(key_column)
        
        chunk_index = 0
        for key_value, group in grouped:
            # Convert group to text for token counting
            group_text = self._dataframe_to_text(group, preserve_headers)
            
            # Estimate token count
            if tokenizer:
                try:
                    tokens = tokenizer.encode(group_text)
                    token_count = len(tokens)
                except:
                    # Fallback to character-based estimation
                    token_count = len(group_text) // 4
            else:
                # Rough estimation: ~4 characters per token
                token_count = len(group_text) // 4
            
            # Split into chunks if exceeds token limit
            if token_count <= token_limit:
                # Save entire group as one chunk
                chunks.append(group.copy())
                
                metadata = self.create_chunk_metadata(
                    chunk=group,
                    chunk_index=chunk_index,
                    start_idx=group.index[0],
                    end_idx=group.index[-1],
                    original_df=dataframe,
                    extra_metadata={
                        'key_column': key_column,
                        'key_value': str(key_value),
                        'chunking_method': 'document_based',
                        'token_count': token_count,
                        'token_limit': token_limit,
                        'group_size': len(group),
                        'is_subchunk': False
                    }
                )
                metadata_list.append(metadata)
                chunk_index += 1
            else:
                # Split group into sub-chunks
                num_chunks = (token_count // token_limit) + 1
                chunk_size = len(group) // num_chunks
                
                for i in range(num_chunks):
                    start_idx = i * chunk_size
                    end_idx = (i + 1) * chunk_size if i < num_chunks - 1 else len(group)
                    
                    if start_idx >= len(group):
                        break
                    
                    sub_group = group.iloc[start_idx:end_idx].copy()
                    chunks.append(sub_group)
                    
                    # Calculate token count for sub-chunk
                    sub_text = self._dataframe_to_text(sub_group, preserve_headers)
                    if tokenizer:
                        try:
                            sub_tokens = tokenizer.encode(sub_text)
                            sub_token_count = len(sub_tokens)
                        except:
                            sub_token_count = len(sub_text) // 4
                    else:
                        sub_token_count = len(sub_text) // 4
                    
                    metadata = self.create_chunk_metadata(
                        chunk=sub_group,
                        chunk_index=chunk_index,
                        start_idx=group.index[start_idx] if start_idx < len(group.index) else group.index[-1],
                        end_idx=group.index[end_idx - 1] if end_idx > 0 and end_idx <= len(group.index) else group.index[-1],
                        original_df=dataframe,
                        extra_metadata={
                            'key_column': key_column,
                            'key_value': str(key_value),
                            'chunking_method': 'document_based',
                            'token_count': sub_token_count,
                            'token_limit': token_limit,
                            'group_size': len(group),
                            'subchunk_index': i + 1,
                            'total_subchunks': num_chunks,
                            'is_subchunk': True
                        }
                    )
                    metadata_list.append(metadata)
                    chunk_index += 1
        
        quality_report = self.assess_chunk_quality(chunks, dataframe)
        
        return ChunkingResult(
            chunks=chunks,
            metadata=metadata_list,
            method=self.name,
            total_chunks=len(chunks),
            quality_report=quality_report
        )
    
    def _dataframe_to_text(self, df: pd.DataFrame, preserve_headers: bool = True) -> str:
        """Convert DataFrame to text representation for token counting"""
        if df.empty:
            return ""
        
        text_parts = []
        
        # Add headers if requested
        if preserve_headers:
            headers = ", ".join(df.columns.astype(str))
            text_parts.append(headers)
        
        # Add rows
        for _, row in df.iterrows():
            row_text = ", ".join([str(val) if pd.notna(val) else "" for val in row])
            text_parts.append(row_text)
        
        return "\n".join(text_parts)

class SemanticChunker(BaseChunker):
    """Semantic chunking - groups rows based on semantic similarity using embeddings"""
    
    def __init__(self):
        super().__init__("semantic")
    
    def chunk(self, dataframe: pd.DataFrame, n_clusters: int = 5, 
              model_name: str = "all-MiniLM-L6-v2", **kwargs) -> ChunkingResult:
        """
        Chunk dataframe using semantic clustering
        
        Args:
            dataframe: Input DataFrame
            n_clusters: Number of semantic clusters
            model_name: Embedding model name
            
        Returns:
            ChunkingResult with semantic chunks
        """
        print(f"🔍 [SEMANTIC] Starting semantic chunking with {n_clusters} clusters using {model_name}")
        print(f"🔍 [SEMANTIC] Input DataFrame: {dataframe.shape[0]} rows, {dataframe.shape[1]} columns")
        print(f"🔍 [SEMANTIC] Dependencies - Sentence Transformers: {SENTENCE_TRANSFORMERS_AVAILABLE}, Sklearn: {SKLEARN_AVAILABLE}")
        
        self.validate_input(dataframe)
        
        if not SENTENCE_TRANSFORMERS_AVAILABLE or not SKLEARN_AVAILABLE:
            print("⚠️ [SEMANTIC] Missing dependencies, using fallback chunking")
            warnings.warn("Semantic chunking requires sentence-transformers and scikit-learn. Using fallback.")
            return self._chunk_fallback(dataframe, n_clusters, **kwargs)
        
        try:
            print(f"🔍 [SEMANTIC] Attempting semantic chunking with embeddings")
            result = self._chunk_with_embeddings(dataframe, n_clusters, model_name, **kwargs)
            print(f"✅ [SEMANTIC] Semantic chunking successful: {result.total_chunks} chunks created")
            return result
        except Exception as e:
            print(f"❌ [SEMANTIC] Semantic chunking failed: {e}. Using fallback.")
            warnings.warn(f"Semantic chunking failed: {e}. Using fallback.")
            fallback_result = self._chunk_fallback(dataframe, n_clusters, **kwargs)
            print(f"✅ [SEMANTIC] Fallback chunking complete: {fallback_result.total_chunks} chunks")
            return fallback_result
    
    def _chunk_with_embeddings(self, dataframe: pd.DataFrame, n_clusters: int, model_name: str, **kwargs) -> ChunkingResult:
        """Semantic chunking using embeddings and clustering"""
        # Convert rows to sentences
        sentences = []
        for _, row in dataframe.iterrows():
            row_text = " ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
            sentences.append(row_text)
        
        # Generate embeddings
        model = SentenceTransformer(model_name)
        embeddings = model.encode(sentences)
        
        # Cluster embeddings
        n_clusters = min(n_clusters, len(sentences))  # Can't have more clusters than sentences
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(embeddings)
        
        # Group rows by cluster
        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(dataframe.index[idx])
        
        # Create chunks from clusters
        chunks = []
        metadata_list = []
        
        for cluster_idx, row_indices in clusters.items():
            cluster_df = dataframe.loc[row_indices].copy()
            
            # Create combined text for this cluster
            cluster_texts = [sentences[dataframe.index.get_loc(idx)] for idx in row_indices]
            combined_text = " ".join(cluster_texts)
            
            # Add text column to chunk
            cluster_df_with_text = cluster_df.copy()
            cluster_df_with_text['text'] = combined_text
            
            chunks.append(cluster_df_with_text)
            
            metadata = self.create_chunk_metadata(
                chunk=cluster_df_with_text,
                chunk_index=cluster_idx,
                start_idx=min(row_indices),
                end_idx=max(row_indices),
                original_df=dataframe,
                extra_metadata={
                    'cluster_id': cluster_idx,
                    'cluster_size': len(row_indices),
                    'n_clusters_param': n_clusters,
                    'model_name': model_name,
                    'chunking_method': 'semantic_clustering',
                    'text_length': len(combined_text)
                }
            )
            metadata_list.append(metadata)
        
        quality_report = self.assess_chunk_quality(chunks, dataframe)
        
        return ChunkingResult(
            chunks=chunks,
            metadata=metadata_list,
            method=self.name,
            total_chunks=len(chunks),
            quality_report=quality_report
        )
    
    def _chunk_fallback(self, dataframe: pd.DataFrame, n_clusters: int, **kwargs) -> ChunkingResult:
        """Fallback semantic chunking without embeddings"""
        # Simple hash-based clustering as fallback
        chunks = []
        metadata_list = []
        
        # Create simple hash-based groups
        chunk_size = max(1, len(dataframe) // n_clusters)
        
        for i in range(n_clusters):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(dataframe))
            
            if start_idx >= len(dataframe):
                break
            
            chunk_df = dataframe.iloc[start_idx:end_idx].copy()
            
            # Add simple text representation
            chunk_text = " ".join([
                " ".join([str(val) for val in row if pd.notna(val)]) 
                for _, row in chunk_df.iterrows()
            ])
            chunk_df['text'] = chunk_text
            
            chunks.append(chunk_df)
            
            metadata = self.create_chunk_metadata(
                chunk=chunk_df,
                chunk_index=i,
                start_idx=start_idx,
                end_idx=end_idx - 1,
                original_df=dataframe,
                extra_metadata={
                    'cluster_id': i,
                    'cluster_size': len(chunk_df),
                    'n_clusters_param': n_clusters,
                    'chunking_method': 'semantic_fallback',
                    'text_length': len(chunk_text)
                }
            )
            metadata_list.append(metadata)
        
        quality_report = self.assess_chunk_quality(chunks, dataframe)
        
        return ChunkingResult(
            chunks=chunks,
            metadata=metadata_list,
            method=self.name,
            total_chunks=len(chunks),
            quality_report=quality_report
        )

# Factory function
def create_chunker(method: str) -> BaseChunker:
    """
    Factory function to create chunkers
    
    Args:
        method: Chunking method ('fixed', 'recursive', 'document_based', 'semantic')
        
    Returns:
        Appropriate chunker instance
    """
    if method == 'fixed' or method == 'fixed_size':
        return FixedSizeChunker()
    elif method == 'recursive':
        return RecursiveChunker()
    elif method == 'document_based' or method == 'document':
        return DocumentBasedChunker()
    elif method == 'semantic':
        return SemanticChunker()
    else:
        raise ValueError(f"Unknown chunking method: {method}")

# Convenience functions for backward compatibility
def chunk_fixed(df: pd.DataFrame, chunk_size: int = 100, overlap: int = 0) -> ChunkingResult:
    """Fixed size chunking convenience function"""
    chunker = FixedSizeChunker()
    return chunker.chunk(df, chunk_size=chunk_size, overlap=overlap)

def chunk_recursive(df: pd.DataFrame, chunk_size: int = 400, overlap: int = 50) -> ChunkingResult:
    """Recursive chunking convenience function"""
    chunker = RecursiveChunker()
    return chunker.chunk(df, chunk_size=chunk_size, overlap=overlap)

def chunk_document_based(df: pd.DataFrame, key_column: str, token_limit: int = 2000, 
                        model_name: str = "gpt-4") -> ChunkingResult:
    """Document-based chunking convenience function"""
    chunker = DocumentBasedChunker()
    return chunker.chunk(df, key_column=key_column, token_limit=token_limit, model_name=model_name)

def chunk_semantic(df: pd.DataFrame, n_clusters: int = 5, 
                  model_name: str = "all-MiniLM-L6-v2") -> ChunkingResult:
    """Semantic chunking convenience function"""
    chunker = SemanticChunker()
    return chunker.chunk(df, n_clusters=n_clusters, model_name=model_name)

def chunk_dataframe(df: pd.DataFrame, method: str = "fixed", **kwargs) -> ChunkingResult:
    """
    Main chunking function that routes to appropriate chunker
    
    Args:
        df: Input DataFrame
        method: Chunking method
        **kwargs: Method-specific parameters
        
    Returns:
        ChunkingResult
    """
    chunker = create_chunker(method)
    return chunker.chunk(df, **kwargs)
