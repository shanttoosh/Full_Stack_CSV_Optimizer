"""
Complete vector storage module with ChromaDB and FAISS support.
Includes the fixed version of your storing.txt plus new FAISS implementation.
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import numpy as np
import json
import os
import pickle
import warnings
from abc import ABC, abstractmethod

# ChromaDB Support
try:
    import chromadb
    from chromadb import Client
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except Exception:
    chromadb = None
    CHROMADB_AVAILABLE = False
    warnings.warn("ChromaDB not available. Install with: pip install chromadb")

# FAISS Support  
try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    faiss = None
    FAISS_AVAILABLE = False
    warnings.warn("FAISS not available. Install with: pip install faiss-cpu")

@dataclass
class VectorRecord:
    """Standard vector record for both storage backends"""
    id: str
    embedding: Union[list, np.ndarray]
    metadata: Dict[str, Any]
    document: Optional[str] = None

def _sanitize_metadata(md: Optional[Dict[str, Any]], fallback_id: str) -> Dict[str, Any]:
    """Sanitize metadata for storage compatibility"""
    safe: Dict[str, Any] = {}
    if md:
        for k, v in md.items():
            try:
                key = str(k)
                if v is None:
                    continue
                if isinstance(v, (str, int, float, bool)):
                    safe[key] = v
                else:
                    safe[key] = str(v)
            except Exception:
                continue
    if not safe:
        safe = {"chunk_id": str(fallback_id)}
    return safe

# Abstract Base Class
class BaseVectorStore(ABC):
    """Abstract base class for vector stores"""
    
    @abstractmethod
    def add(self, records: List[VectorRecord]):
        """Add vector records to the store"""
        pass
    
    @abstractmethod
    def query(self, query_embeddings: List[list], n_results: int = 5, where: Optional[Dict[str, Any]] = None):
        """Query the vector store"""
        pass
    
    @abstractmethod
    def reset(self):
        """Reset/clear the vector store"""
        pass

# ChromaDB Implementation (your existing code with fixes)
class ChromaVectorStore(BaseVectorStore):
    """ChromaDB-based vector storage"""

    def __init__(self, persist_directory: str = ".chroma", collection_name: str = "csv_chunks"):
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB is not installed. Please install it to use ChromaVectorStore.")
        
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.client = None
        self.collection = None

    def connect(self):
        """Connect to ChromaDB"""
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB is not installed. Please install it to use ChromaVectorStore.")
        
        # Ensure directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        return self

    def get_or_create_collection(self, metadata: Optional[Dict[str, Any]] = None):
        """Get or create a collection"""
        if self.client is None:
            self.connect()
        
        default_md = {"created_by": "csv_chunking_optimizer", "purpose": "chunk_storage"}
        md = metadata if (metadata and len(metadata) > 0) else default_md
        
        self.collection = self.client.get_or_create_collection(name=self.collection_name, metadata=md)
        return self.collection

    def add(self, records: List[VectorRecord]):
        """Add records to ChromaDB"""
        if self.collection is None:
            self.get_or_create_collection()
        
        if not records:
            return
        
        ids = [r.id for r in records]
        embeddings = []
        
        for r in records:
            if isinstance(r.embedding, np.ndarray):
                embeddings.append(r.embedding.tolist())
            else:
                embeddings.append(r.embedding)
        
        metadatas = [_sanitize_metadata(r.metadata, r.id) for r in records]
        documents = []
        
        for r in records:
            if isinstance(r.document, str):
                documents.append(r.document)
            elif r.document is None:
                documents.append("")
            else:
                documents.append(str(r.document))
        
        try:
            self.collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)
        except Exception as e:
            # If add fails, try upsert
            warnings.warn(f"Add failed, trying upsert: {e}")
            self.collection.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

    def upsert(self, records: List[VectorRecord]):
        """Upsert records to ChromaDB"""
        if self.collection is None:
            self.get_or_create_collection()
        
        if not records:
            return
        
        ids = [r.id for r in records]
        embeddings = []
        
        for r in records:
            if isinstance(r.embedding, np.ndarray):
                embeddings.append(r.embedding.tolist())
            else:
                embeddings.append(r.embedding)
        
        metadatas = [_sanitize_metadata(r.metadata, r.id) for r in records]
        documents = []
        
        for r in records:
            if isinstance(r.document, str):
                documents.append(r.document)
            elif r.document is None:
                documents.append("")
            else:
                documents.append(str(r.document))
        
        self.collection.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

    def query(self, query_embeddings: List[list], n_results: int = 5, where: Optional[Dict[str, Any]] = None):
        """Query ChromaDB"""
        if self.collection is None:
            self.get_or_create_collection()
        
        return self.collection.query(query_embeddings=query_embeddings, n_results=n_results, where=where)

    def reset(self):
        """Reset ChromaDB collection"""
        if self.client is None:
            self.connect()
        
        try:
            # Delete existing collection
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass  # Collection might not exist
        
        # Recreate collection
        self.get_or_create_collection()

    def reset_collection(self):
        """Legacy method name for backward compatibility"""
        return self.reset()

# FAISS Implementation
class FAISSVectorStore(BaseVectorStore):
    """FAISS-based vector storage for high-performance similarity search"""

    def __init__(self, dimension: int = 384, index_type: str = "flat", persist_directory: str = ".faiss"):
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS is not installed. Please install it to use FAISSVectorStore.")
        
        self.dimension = dimension
        self.persist_directory = persist_directory
        self.index_type = index_type.lower()
        self.index = None
        self.metadata_store = {}
        self.id_to_index = {}
        self.index_to_id = {}
        self.documents = {}
        
        # Create persist directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize index
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize FAISS index"""
        if self.index_type == "flat":
            # Flat index with inner product (cosine similarity when normalized)
            self.index = faiss.IndexFlatIP(self.dimension)
        elif self.index_type == "ivf":
            # IVF index for larger datasets
            quantizer = faiss.IndexFlatIP(self.dimension)
            self.index = faiss.IndexIVFFlat(quantizer, self.dimension, 100)  # 100 clusters
        elif self.index_type == "hnsw":
            # HNSW index for very fast search
            self.index = faiss.IndexHNSWFlat(self.dimension, 32)
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}. Use 'flat', 'ivf', or 'hnsw'")
    
    def add(self, records: List[VectorRecord]):
        """Add records to FAISS index"""
        if not records:
            return
        
        embeddings = []
        for i, record in enumerate(records):
            # Convert embedding to numpy array
            if isinstance(record.embedding, list):
                embedding = np.array(record.embedding, dtype=np.float32)
            else:
                embedding = record.embedding.astype(np.float32)
            
            # Normalize for cosine similarity (important for IndexFlatIP)
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            
            embeddings.append(embedding)
            
            # Store metadata and documents
            current_index = self.index.ntotal + i
            self.id_to_index[record.id] = current_index
            self.index_to_id[current_index] = record.id
            self.metadata_store[record.id] = record.metadata or {}
            self.documents[record.id] = record.document or ""
        
        # Add to FAISS index
        embeddings_matrix = np.vstack(embeddings)
        
        # Train index if necessary (for IVF)
        if self.index_type == "ivf" and not self.index.is_trained:
            self.index.train(embeddings_matrix)
        
        self.index.add(embeddings_matrix)
    
    def query(self, query_embeddings: List[list], n_results: int = 5, where: Optional[Dict[str, Any]] = None):
        """Query FAISS index"""
        if self.index.ntotal == 0:
            return {"ids": [[]], "distances": [[]], "metadatas": [[]], "documents": [[]]}
        
        # Convert query embeddings
        query_matrix = np.array(query_embeddings, dtype=np.float32)
        
        # Normalize for cosine similarity
        for i in range(query_matrix.shape[0]):
            norm = np.linalg.norm(query_matrix[i])
            if norm > 0:
                query_matrix[i] = query_matrix[i] / norm
        
        # Search
        distances, indices = self.index.search(query_matrix, n_results)
        
        # Format results to match ChromaDB format
        results = {"ids": [], "distances": [], "metadatas": [], "documents": []}
        
        for i, (dist_row, idx_row) in enumerate(zip(distances, indices)):
            ids = []
            metadatas = []
            documents = []
            valid_distances = []
            
            for dist, idx in zip(dist_row, idx_row):
                if idx != -1:  # Valid result
                    record_id = self.index_to_id.get(idx)
                    if record_id:
                        # Apply metadata filtering if specified
                        if where:
                            metadata = self.metadata_store.get(record_id, {})
                            if not self._matches_filter(metadata, where):
                                continue
                        
                        ids.append(record_id)
                        metadatas.append(self.metadata_store.get(record_id, {}))
                        documents.append(self.documents.get(record_id, ""))
                        valid_distances.append(float(dist))
            
            results["ids"].append(ids)
            results["distances"].append(valid_distances)
            results["metadatas"].append(metadatas)
            results["documents"].append(documents)
        
        return results
    
    def _matches_filter(self, metadata: Dict[str, Any], where: Dict[str, Any]) -> bool:
        """Check if metadata matches filter conditions"""
        for key, value in where.items():
            if key not in metadata or metadata[key] != value:
                return False
        return True
    
    def save(self):
        """Save FAISS index and metadata to disk"""
        # Save FAISS index
        index_path = os.path.join(self.persist_directory, "index.faiss")
        faiss.write_index(self.index, index_path)
        
        # Save metadata
        metadata_path = os.path.join(self.persist_directory, "metadata.pkl")
        with open(metadata_path, "wb") as f:
            pickle.dump({
                "metadata_store": self.metadata_store,
                "id_to_index": self.id_to_index,
                "index_to_id": self.index_to_id,
                "documents": self.documents,
                "dimension": self.dimension,
                "index_type": self.index_type
            }, f)
    
    def load(self):
        """Load FAISS index and metadata from disk"""
        index_path = os.path.join(self.persist_directory, "index.faiss")
        metadata_path = os.path.join(self.persist_directory, "metadata.pkl")
        
        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        
        if os.path.exists(metadata_path):
            with open(metadata_path, "rb") as f:
                data = pickle.load(f)
                self.metadata_store = data.get("metadata_store", {})
                self.id_to_index = data.get("id_to_index", {})
                self.index_to_id = data.get("index_to_id", {})
                self.documents = data.get("documents", {})
                
                # Verify dimension compatibility
                saved_dimension = data.get("dimension", self.dimension)
                if saved_dimension != self.dimension:
                    warnings.warn(f"Dimension mismatch: saved {saved_dimension}, current {self.dimension}")
    
    def reset(self):
        """Reset FAISS index and clear all data"""
        # Clear in-memory data
        self.metadata_store = {}
        self.id_to_index = {}
        self.index_to_id = {}
        self.documents = {}
        
        # Reinitialize index
        self._initialize_index()
        
        # Remove saved files
        index_path = os.path.join(self.persist_directory, "index.faiss")
        metadata_path = os.path.join(self.persist_directory, "metadata.pkl")
        
        for path in [index_path, metadata_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    warnings.warn(f"Failed to remove {path}: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the FAISS index"""
        return {
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "index_type": self.index_type,
            "is_trained": getattr(self.index, 'is_trained', True),
            "memory_usage_bytes": self.index.ntotal * self.dimension * 4  # float32
        }

# Factory Functions
def create_vector_store(store_type: str = "chroma", **kwargs) -> BaseVectorStore:
    """
    Factory function to create vector stores
    
    Args:
        store_type: Type of store ('chroma' or 'faiss')
        **kwargs: Store-specific parameters
        
    Returns:
        Vector store instance
    """
    store_type = store_type.lower()
    
    if store_type == "chroma":
        return ChromaVectorStore(**kwargs)
    elif store_type == "faiss":
        return FAISSVectorStore(**kwargs)
    else:
        raise ValueError(f"Unsupported vector store type: {store_type}. Use 'chroma' or 'faiss'")

def get_available_stores() -> List[str]:
    """Get list of available vector store types"""
    available = []
    if CHROMADB_AVAILABLE:
        available.append("chroma")
    if FAISS_AVAILABLE:
        available.append("faiss")
    return available

def recommend_store(num_vectors: int, dimension: int = 384) -> str:
    """
    Recommend vector store based on dataset size
    
    Args:
        num_vectors: Expected number of vectors
        dimension: Vector dimension
        
    Returns:
        Recommended store type
    """
    if not CHROMADB_AVAILABLE and not FAISS_AVAILABLE:
        raise RuntimeError("No vector stores available. Install chromadb or faiss-cpu.")
    
    # For small datasets, ChromaDB is simpler
    if num_vectors < 1000:
        return "chroma" if CHROMADB_AVAILABLE else "faiss"
    
    # For larger datasets, FAISS is more efficient
    if num_vectors > 10000:
        return "faiss" if FAISS_AVAILABLE else "chroma"
    
    # For medium datasets, prefer FAISS if available
    return "faiss" if FAISS_AVAILABLE else "chroma"

# Utility functions for working with embeddings
def convert_embeddings_to_records(embedded_chunks: List[Any]) -> List[VectorRecord]:
    """
    Convert EmbeddedChunk objects to VectorRecord objects
    
    Args:
        embedded_chunks: List of EmbeddedChunk objects from embedding module
        
    Returns:
        List of VectorRecord objects
    """
    records = []
    
    for chunk in embedded_chunks:
        # Convert embedding to list if it's numpy array
        embedding = chunk.embedding
        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()
        
        # Extract metadata
        metadata = {}
        if hasattr(chunk, 'metadata') and chunk.metadata:
            if hasattr(chunk.metadata, '__dict__'):
                metadata = chunk.metadata.__dict__.copy()
            else:
                metadata = dict(chunk.metadata)
        
        # Create VectorRecord
        record = VectorRecord(
            id=chunk.id,
            embedding=embedding,
            metadata=metadata,
            document=getattr(chunk, 'document', None)
        )
        records.append(record)
    
    return records

def store_embeddings(embedded_chunks: List[Any], 
                    store_type: str = "chroma",
                    **store_kwargs) -> BaseVectorStore:
    """
    Convenience function to store embeddings
    
    Args:
        embedded_chunks: List of EmbeddedChunk objects
        store_type: Vector store type
        **store_kwargs: Store-specific parameters
        
    Returns:
        Configured vector store with embeddings added
    """
    # Create vector store
    store = create_vector_store(store_type, **store_kwargs)
    
    # Convert embeddings to records
    records = convert_embeddings_to_records(embedded_chunks)
    
    # Add to store
    store.add(records)
    
    # Save if it's FAISS
    if isinstance(store, FAISSVectorStore):
        store.save()
    
    return store
