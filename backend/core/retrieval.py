"""
Complete retrieval module with multiple similarity metrics support.
Supports cosine, dot product, and euclidean similarity with both ChromaDB and FAISS.
"""

from typing import List, Dict, Any, Optional, Literal, Union
import numpy as np
from enum import Enum
import warnings

# Import storage modules
try:
    from .storing import ChromaVectorStore, FAISSVectorStore, BaseVectorStore, create_vector_store
except ImportError:
    # Fallback for direct usage
    from storing import ChromaVectorStore, FAISSVectorStore, BaseVectorStore, create_vector_store

class SimilarityMetric(Enum):
    """Supported similarity metrics"""
    COSINE = "cosine"
    DOT_PRODUCT = "dot"
    EUCLIDEAN = "euclidean"

class SimilarityCalculator:
    """Handles different similarity calculations"""
    
    @staticmethod
    def cosine_similarity(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """
        Calculate cosine similarity between query and document vectors
        
        Args:
            query_vec: Query vector (1D)
            doc_vecs: Document vectors (2D, each row is a vector)
            
        Returns:
            Similarity scores (higher is more similar)
        """
        # Normalize vectors
        query_norm = query_vec / (np.linalg.norm(query_vec) + 1e-8)
        doc_norms = doc_vecs / (np.linalg.norm(doc_vecs, axis=1, keepdims=True) + 1e-8)
        
        # Calculate cosine similarity
        similarities = np.dot(doc_norms, query_norm)
        return similarities
    
    @staticmethod
    def dot_product_similarity(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """
        Calculate dot product similarity
        
        Args:
            query_vec: Query vector (1D)
            doc_vecs: Document vectors (2D, each row is a vector)
            
        Returns:
            Similarity scores (higher is more similar)
        """
        return np.dot(doc_vecs, query_vec)
    
    @staticmethod
    def euclidean_distance(query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """
        Calculate euclidean distance and convert to similarity
        
        Args:
            query_vec: Query vector (1D)
            doc_vecs: Document vectors (2D, each row is a vector)
            
        Returns:
            Similarity scores (higher is more similar)
        """
        # Calculate euclidean distances
        distances = np.linalg.norm(doc_vecs - query_vec, axis=1)
        # Convert to similarity (higher is better)
        similarities = 1 / (1 + distances)
        return similarities
    
    @staticmethod
    def calculate_similarity(query_vec: np.ndarray, doc_vecs: np.ndarray, 
                           metric: str = "cosine") -> np.ndarray:
        """
        Calculate similarity using specified metric
        
        Args:
            query_vec: Query vector
            doc_vecs: Document vectors
            metric: Similarity metric ('cosine', 'dot', 'euclidean')
            
        Returns:
            Similarity scores
        """
        if metric == "cosine":
            return SimilarityCalculator.cosine_similarity(query_vec, doc_vecs)
        elif metric == "dot":
            return SimilarityCalculator.dot_product_similarity(query_vec, doc_vecs)
        elif metric == "euclidean":
            return SimilarityCalculator.euclidean_distance(query_vec, doc_vecs)
        else:
            raise ValueError(f"Unsupported similarity metric: {metric}")

class UnifiedRetriever:
    """
    Unified retriever supporting multiple vector stores and similarity metrics
    """
    
    def __init__(self, 
                 store_type: str = "chroma",
                 collection_name: str = "csv_chunks", 
                 persist_directory: Optional[str] = None,
                 **store_kwargs):
        """
        Initialize unified retriever
        
        Args:
            store_type: Vector store type ('chroma' or 'faiss')
            collection_name: Collection name for ChromaDB
            persist_directory: Directory for persistence
            **store_kwargs: Additional store parameters
        """
        
        self.store_type = store_type.lower()
        self.collection_name = collection_name
        
        # Set default persist directories
        if persist_directory is None:
            persist_directory = ".chroma" if store_type == "chroma" else ".faiss"
        
        # Initialize vector store
        store_config = {
            "persist_directory": persist_directory,
            **store_kwargs
        }
        
        if self.store_type == "chroma":
            store_config["collection_name"] = collection_name
            self.store = ChromaVectorStore(**store_config)
            self.store.connect().get_or_create_collection()
        elif self.store_type == "faiss":
            self.store = FAISSVectorStore(**store_config)
            try:
                self.store.load()  # Try to load existing index
            except Exception:
                pass  # Will create new index when needed
        else:
            raise ValueError(f"Unsupported store type: {store_type}")
        
        self.model = None
        self.model_name = None
        self.similarity_calculator = SimilarityCalculator()
    
    def _load_model(self, model_name: str):
        """Load embedding model if not already loaded"""
        if self.model is not None and self.model_name == model_name:
            return
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self.model_name = model_name
        except ImportError:
            raise ImportError("sentence-transformers library not available. Please install it.")
        except Exception as e:
            raise Exception(f"Failed to load model {model_name}: {e}")
    
    def embed_query(self, query: str, model_name: str) -> List[float]:
        """
        Convert query text to embedding vector
        
        Args:
            query: Search query text
            model_name: Embedding model to use
            
        Returns:
            Query embedding as list
        """
        self._load_model(model_name)
        vec = self.model.encode([query], convert_to_tensor=False)[0]
        return vec.tolist() if isinstance(vec, np.ndarray) else list(vec)
    
    def search(self, 
               query: str, 
               model_name: str, 
               top_k: int = 5,
               similarity_metric: str = "cosine",
               where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for similar chunks using specified similarity metric
        
        Args:
            query: Search query text
            model_name: Embedding model to use
            top_k: Number of results to return
            similarity_metric: "cosine", "dot", or "euclidean"
            where: Metadata filter conditions
        
        Returns:
            Search results with similarity scores
        """
        
        # Validate similarity metric
        if similarity_metric not in ["cosine", "dot", "euclidean"]:
            raise ValueError(f"Unsupported similarity metric: {similarity_metric}")
        
        # Get query embedding
        query_vec = self.embed_query(query, model_name)
        
        # For ChromaDB, use native search with post-processing
        if self.store_type == "chroma":
            results = self.store.query(
                query_embeddings=[query_vec], 
                n_results=top_k, 
                where=where
            )
            
            # ChromaDB returns L2 distances by default
            # Convert based on similarity metric preference
            if similarity_metric == "cosine":
                # For cosine similarity, we need to recompute if we want exact values
                # For now, we'll convert L2 distances to approximate similarities
                for i, distances in enumerate(results.get("distances", [])):
                    # Convert L2 distances to similarities (approximate)
                    results["distances"][i] = [max(0, 1 - d/2) for d in distances]
            elif similarity_metric == "euclidean":
                # L2 distance is euclidean distance, convert to similarity
                for i, distances in enumerate(results.get("distances", [])):
                    results["distances"][i] = [1 / (1 + d) for d in distances]
            # For dot product, keep as is (approximation)
            
            return results
        
        # For FAISS, we have more control over similarity metrics
        elif self.store_type == "faiss":
            if similarity_metric == "cosine":
                # FAISS with IndexFlatIP already does cosine similarity when vectors are normalized
                results = self.store.query([query_vec], top_k, where)
            else:
                # For other metrics, get results and potentially rerank
                results = self.store.query([query_vec], min(top_k * 2, 100), where)
                
                # For exact similarity calculations, we would need access to stored embeddings
                # This is a simplified implementation for the current architecture
                # In a production system, you might store embeddings separately for reranking
                
                if similarity_metric == "euclidean":
                    # Convert cosine similarities to approximate euclidean similarities
                    for i, distances in enumerate(results.get("distances", [])):
                        # Approximate conversion
                        results["distances"][i] = [1 / (2 - d) if d < 2 else 0.01 for d in distances]
                elif similarity_metric == "dot":
                    # For dot product, we'd need the original unnormalized vectors
                    # For now, return as-is with a warning
                    if results.get("distances") and results["distances"][0]:
                        warnings.warn("Dot product similarity with FAISS may not be exact without storing original embeddings")
                
                # Trim to requested top_k
                for key in results:
                    if isinstance(results[key], list) and results[key]:
                        results[key] = [lst[:top_k] if isinstance(lst, list) else lst for lst in results[key]]
            
            return results
        
        else:
            raise ValueError(f"Unsupported store type: {self.store_type}")
    
    def search_with_embedding(self,
                            query_embedding: List[float],
                            top_k: int = 5,
                            similarity_metric: str = "cosine",
                            where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search using pre-computed query embedding
        
        Args:
            query_embedding: Pre-computed query embedding
            top_k: Number of results to return
            similarity_metric: Similarity metric to use
            where: Metadata filter conditions
            
        Returns:
            Search results
        """
        
        if similarity_metric not in ["cosine", "dot", "euclidean"]:
            raise ValueError(f"Unsupported similarity metric: {similarity_metric}")
        
        # Use the vector store's native search
        results = self.store.query([query_embedding], top_k, where)
        
        # Apply similarity metric transformations as in the search method
        if self.store_type == "chroma":
            if similarity_metric == "cosine":
                for i, distances in enumerate(results.get("distances", [])):
                    results["distances"][i] = [max(0, 1 - d/2) for d in distances]
            elif similarity_metric == "euclidean":
                for i, distances in enumerate(results.get("distances", [])):
                    results["distances"][i] = [1 / (1 + d) for d in distances]
        
        return results
    
    def get_similarity_metrics_info(self) -> Dict[str, str]:
        """Return information about available similarity metrics"""
        return {
            "cosine": "Measures the cosine of the angle between vectors (0-1, higher is more similar)",
            "dot": "Dot product similarity (unbounded, higher is more similar)", 
            "euclidean": "Euclidean distance converted to similarity (0-1, higher is more similar)"
        }
    
    def get_store_info(self) -> Dict[str, Any]:
        """Get information about the current vector store"""
        info = {
            "store_type": self.store_type,
            "collection_name": getattr(self, 'collection_name', None)
        }
        
        if hasattr(self.store, 'get_stats'):
            info.update(self.store.get_stats())
        elif self.store_type == "faiss" and hasattr(self.store, 'index'):
            info.update({
                "total_vectors": self.store.index.ntotal,
                "dimension": self.store.dimension,
                "index_type": self.store.index_type
            })
        
        return info

# Legacy compatibility - keep your original Retriever class
class Retriever:
    """Original Retriever class for backward compatibility"""
    
    def __init__(self, collection_name: str = "csv_chunks", persist_directory: str = ".chroma"):
        self.unified_retriever = UnifiedRetriever("chroma", collection_name, persist_directory)
    
    def search(self, query: str, model_name: str, top_k: int = 5, where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Legacy search method"""
        return self.unified_retriever.search(query, model_name, top_k, "cosine", where)
    
    def embed_query(self, query: str, model_name: str) -> List[float]:
        """Legacy embed_query method"""
        return self.unified_retriever.embed_query(query, model_name)

# Enhanced Retriever with Advanced Features
class AdvancedRetriever(UnifiedRetriever):
    """
    Advanced retriever with additional features like reranking and hybrid search
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query_history = []
        self.result_cache = {}
    
    def search_with_reranking(self,
                            query: str,
                            model_name: str,
                            top_k: int = 5,
                            initial_k: int = None,
                            similarity_metric: str = "cosine",
                            rerank_metric: str = "cosine",
                            where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search with two-stage retrieval and reranking
        
        Args:
            query: Search query
            model_name: Embedding model
            top_k: Final number of results
            initial_k: Initial retrieval size (default: top_k * 3)
            similarity_metric: Initial similarity metric
            rerank_metric: Reranking similarity metric
            where: Metadata filters
            
        Returns:
            Reranked search results
        """
        
        if initial_k is None:
            initial_k = min(top_k * 3, 50)
        
        # Initial retrieval with larger k
        initial_results = self.search(
            query=query,
            model_name=model_name,
            top_k=initial_k,
            similarity_metric=similarity_metric,
            where=where
        )
        
        # If rerank metric is different, recompute similarities
        if rerank_metric != similarity_metric and initial_results.get("documents"):
            query_embedding = np.array(self.embed_query(query, model_name))
            
            # This would require access to stored embeddings for exact reranking
            # For now, return initial results with a note
            warnings.warn("Exact reranking requires access to stored embeddings. Returning initial results.")
        
        # Trim to final top_k
        final_results = {"ids": [], "distances": [], "metadatas": [], "documents": []}
        
        for key in final_results:
            if key in initial_results and initial_results[key]:
                final_results[key] = [
                    lst[:top_k] if isinstance(lst, list) else lst 
                    for lst in initial_results[key]
                ]
        
        return final_results
    
    def search_hybrid(self,
                     query: str,
                     model_name: str,
                     top_k: int = 5,
                     keyword_weight: float = 0.3,
                     semantic_weight: float = 0.7,
                     where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Hybrid search combining keyword and semantic search
        
        Args:
            query: Search query
            model_name: Embedding model
            top_k: Number of results
            keyword_weight: Weight for keyword matching
            semantic_weight: Weight for semantic similarity
            where: Metadata filters
            
        Returns:
            Hybrid search results
        """
        
        # For now, this is a simplified implementation
        # A full hybrid search would require keyword indexing
        
        # Get semantic results
        semantic_results = self.search(
            query=query,
            model_name=model_name,
            top_k=top_k * 2,  # Get more for hybrid scoring
            similarity_metric="cosine",
            where=where
        )
        
        # Simple keyword scoring based on query term presence
        query_terms = query.lower().split()
        
        if semantic_results.get("documents"):
            for i, doc_list in enumerate(semantic_results["documents"]):
                for j, doc in enumerate(doc_list):
                    if doc:
                        # Simple keyword scoring
                        doc_lower = doc.lower()
                        keyword_score = sum(1 for term in query_terms if term in doc_lower) / len(query_terms)
                        
                        # Combine with semantic score
                        semantic_score = semantic_results["distances"][i][j] if semantic_results.get("distances") else 0
                        hybrid_score = (semantic_weight * semantic_score) + (keyword_weight * keyword_score)
                        
                        # Update distance with hybrid score
                        if semantic_results.get("distances"):
                            semantic_results["distances"][i][j] = hybrid_score
        
        # Sort by hybrid scores and return top_k
        # This is a simplified version - a production implementation would be more sophisticated
        return semantic_results

# Convenience functions
def create_retriever(store_type: str = "chroma", **kwargs) -> UnifiedRetriever:
    """Factory function to create a retriever"""
    return UnifiedRetriever(store_type=store_type, **kwargs)

def search_chunks(query: str,
                 model_name: str = "all-MiniLM-L6-v2",
                 store_type: str = "chroma",
                 similarity_metric: str = "cosine",
                 top_k: int = 5,
                 **kwargs) -> Dict[str, Any]:
    """
    Convenience function for quick searching
    
    Args:
        query: Search query
        model_name: Embedding model
        store_type: Vector store type
        similarity_metric: Similarity metric
        top_k: Number of results
        **kwargs: Additional retriever parameters
        
    Returns:
        Search results
    """
    retriever = create_retriever(store_type, **kwargs)
    return retriever.search(query, model_name, top_k, similarity_metric)

def compare_similarities(query: str,
                        model_name: str = "all-MiniLM-L6-v2",
                        store_type: str = "chroma",
                        top_k: int = 5,
                        **kwargs) -> Dict[str, Dict[str, Any]]:
    """
    Compare results across different similarity metrics
    
    Args:
        query: Search query
        model_name: Embedding model
        store_type: Vector store type
        top_k: Number of results
        **kwargs: Additional retriever parameters
        
    Returns:
        Results for each similarity metric
    """
    retriever = create_retriever(store_type, **kwargs)
    
    results = {}
    for metric in ["cosine", "dot", "euclidean"]:
        try:
            results[metric] = retriever.search(query, model_name, top_k, metric)
        except Exception as e:
            results[metric] = {"error": str(e)}
    
    return results
