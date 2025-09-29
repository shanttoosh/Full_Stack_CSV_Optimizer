# 10. Database Schema

### 🗄️ Vector Database Overview

CSV Chunker Pro uses two vector database systems for storing and retrieving embeddings:

- **ChromaDB**: Default database for development and small-to-medium datasets
- **FAISS**: High-performance database for production and large datasets

Both databases store the same logical schema but with different physical implementations.

### 📊 Logical Data Schema

#### **Core Data Structure**
```
Processing Session
├── Chunks (Text segments from CSV)
├── Embeddings (Vector representations)
├── Metadata (Processing information)
└── Search Index (Optimized for retrieval)
```

#### **Data Relationships**
```
CSV File (1) → Processing Session (1) → Multiple Chunks (N)
Each Chunk (1) → One Embedding (1) + Metadata (1)
Processing Session (1) → One Search Collection (1)
```

### 🔵 ChromaDB Schema

#### **Database Structure**
```
backend/storage/.chroma/
├── chroma.sqlite3              # SQLite database file
├── index/                      # Vector index files
│   ├── collection_uuid.bin     # Binary index data
│   └── collection_uuid.meta    # Index metadata
└── collections/                # Collection-specific data
    └── collection_uuid/
        ├── data.parquet        # Document and metadata storage
        └── embeddings.bin      # Vector embeddings
```

#### **Collection Schema**
Each processing session creates a unique collection:

**Collection Name Format**: `collection_{processing_id}`
```python
# Example: collection_a7f1bd91-3725-4424-99af-42458b711ebe
```

**Collection Contents**:
```python
{
    "ids": [
        "semantic_chunk_0000",
        "semantic_chunk_0001", 
        "semantic_chunk_0002"
    ],
    "embeddings": [
        [0.1, -0.2, 0.5, ...],  # 384-dimensional vector
        [0.3, 0.1, -0.4, ...],  # 384-dimensional vector
        [-0.1, 0.7, 0.2, ...]   # 384-dimensional vector
    ],
    "documents": [
        "Customer ID: 12345, Name: John Doe, Age: 35...",
        "Product: Widget A, Price: $29.99, Category: Electronics...",
        "Order Date: 2025-01-15, Quantity: 2, Total: $59.98..."
    ],
    "metadatas": [
        {
            "chunk_id": "semantic_chunk_0000",
            "chunk_method": "semantic",
            "chunk_number": 1,
            "source_file": "customer_data.csv",
            "embedding_model": "all-MiniLM-L6-v2",
            "vector_dimension": 384,
            "text_length": 284,
            "source_rows": [0, 1, 2, 3, 4],
            "created_at": "2025-09-29T14:30:00Z",
            "processing_id": "a7f1bd91-3725-4424-99af-42458b711ebe"
        }
    ]
}
```

#### **Metadata Field Definitions**
| **Field** | **Type** | **Description** | **Example** |
|-----------|----------|-----------------|-------------|
| `chunk_id` | string | Unique identifier for chunk | `"semantic_chunk_0000"` |
| `chunk_method` | string | Chunking algorithm used | `"semantic"`, `"fixed"`, `"recursive"` |
| `chunk_number` | integer | Sequential chunk number | `1`, `2`, `3` |
| `source_file` | string | Original CSV filename | `"customer_data.csv"` |
| `embedding_model` | string | Model used for embeddings | `"all-MiniLM-L6-v2"` |
| `vector_dimension` | integer | Embedding vector size | `384`, `768` |
| `text_length` | integer | Character count of chunk text | `284` |
| `source_rows` | array | Original CSV row indices | `[0, 1, 2, 3, 4]` |
| `created_at` | string | ISO timestamp | `"2025-09-29T14:30:00Z"` |
| `processing_id` | string | Session identifier | `"a7f1bd91-3725..."` |

#### **ChromaDB Operations**
```python
# Create collection
collection = client.create_collection(
    name=f"collection_{processing_id}",
    metadata={"description": "CSV chunks with embeddings"}
)

# Add documents
collection.add(
    ids=chunk_ids,
    embeddings=embeddings_list,
    documents=chunk_texts,
    metadatas=metadata_list
)

# Query collection
results = collection.query(
    query_embeddings=[query_vector],
    n_results=5,
    where={"chunk_method": "semantic"}  # Optional filtering
)
```

### 🔶 FAISS Schema

#### **Database Structure**
```
backend/storage/.faiss/
├── processing_id.index          # FAISS index file
├── processing_id.metadata.json  # Metadata mapping
└── processing_id.documents.json # Document storage
```

#### **Index Structure**
**Index File**: Binary FAISS index containing vectors
```python
# FAISS Index Properties
index_type = "IndexFlatIP"        # Inner Product (for cosine similarity)
dimension = 384                   # Vector dimension
total_vectors = 25                # Number of stored vectors
```

**Metadata File**: JSON mapping from vector index to metadata
```json
{
  "0": {
    "chunk_id": "semantic_chunk_0000",
    "chunk_method": "semantic",
    "chunk_number": 1,
    "source_file": "customer_data.csv",
    "embedding_model": "all-MiniLM-L6-v2",
    "vector_dimension": 384,
    "text_length": 284,
    "source_rows": [0, 1, 2, 3, 4],
    "created_at": "2025-09-29T14:30:00Z",
    "processing_id": "a7f1bd91-3725-4424-99af-42458b711ebe"
  },
  "1": { ... },
  "2": { ... }
}
```

**Documents File**: JSON mapping from vector index to text content
```json
{
  "0": "Customer ID: 12345, Name: John Doe, Age: 35, Location: New York...",
  "1": "Product: Widget A, Price: $29.99, Category: Electronics...",
  "2": "Order Date: 2025-01-15, Quantity: 2, Total: $59.98..."
}
```

#### **FAISS Operations**
```python
# Create index
index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity

# Add vectors
index.add(embeddings_array)  # numpy array of shape (n_vectors, dimension)

# Save index
faiss.write_index(index, f"backend/storage/.faiss/{processing_id}.index")

# Search index
scores, indices = index.search(query_vector, k=5)
```

### 🔄 Database Comparison

| **Feature** | **ChromaDB** | **FAISS** |
|-------------|--------------|-----------|
| **Setup** | Automatic | Automatic |
| **Storage** | SQLite + Files | Binary Index + JSON |
| **Query Interface** | High-level API | Low-level operations |
| **Metadata Filtering** | Native support | Manual implementation |
| **Similarity Metrics** | Cosine, L2, IP | Configurable |
| **Scalability** | Good (< 1M vectors) | Excellent (> 1M vectors) |
| **Memory Usage** | Higher | Lower |
| **Query Speed** | Good | Excellent |
| **Persistence** | Automatic | Manual save/load |
| **Best For** | Development, small datasets | Production, large datasets |

### 📈 Performance Characteristics

#### **ChromaDB Performance**
```
Vector Count    | Query Time | Memory Usage | Disk Usage
1,000          | ~10ms      | ~50MB       | ~25MB
10,000         | ~50ms      | ~200MB      | ~100MB  
100,000        | ~200ms     | ~1GB        | ~500MB
1,000,000      | ~1s        | ~5GB        | ~2GB
```

#### **FAISS Performance**
```
Vector Count    | Query Time | Memory Usage | Disk Usage
1,000          | ~5ms       | ~20MB       | ~15MB
10,000         | ~20ms      | ~80MB       | ~40MB
100,000        | ~50ms      | ~400MB      | ~200MB
1,000,000      | ~100ms     | ~2GB        | ~1GB
```

### 🔍 Search Query Process

#### **ChromaDB Search Flow**
```python
def search_chromadb(processing_id: str, query: str, top_k: int = 5):
    # 1. Load collection
    collection = client.get_collection(f"collection_{processing_id}")
    
    # 2. Generate query embedding
    query_embedding = embedding_model.encode([query])
    
    # 3. Perform similarity search
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    # 4. Format results
    formatted_results = []
    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0], 
        results['distances'][0]
    )):
        formatted_results.append({
            'rank': i + 1,
            'similarity_score': 1 - distance,  # Convert distance to similarity
            'document': doc,
            'metadata': metadata
        })
    
    return formatted_results
```

#### **FAISS Search Flow**
```python
def search_faiss(processing_id: str, query: str, top_k: int = 5):
    # 1. Load index and metadata
    index = faiss.read_index(f"backend/storage/.faiss/{processing_id}.index")
    
    with open(f"backend/storage/.faiss/{processing_id}.metadata.json") as f:
        metadata = json.load(f)
    
    with open(f"backend/storage/.faiss/{processing_id}.documents.json") as f:
        documents = json.load(f)
    
    # 2. Generate query embedding
    query_embedding = embedding_model.encode([query])
    
    # 3. Normalize for cosine similarity
    faiss.normalize_L2(query_embedding)
    
    # 4. Search index
    scores, indices = index.search(query_embedding, top_k)
    
    # 5. Format results
    formatted_results = []
    for i, (idx, score) in enumerate(zip(indices[0], scores[0])):
        formatted_results.append({
            'rank': i + 1,
            'similarity_score': float(score),
            'document': documents[str(idx)],
            'metadata': metadata[str(idx)]
        })
    
    return formatted_results
```

### 🛠️ Database Maintenance

#### **ChromaDB Maintenance**
```python
# Collection management
def list_collections():
    return client.list_collections()

def delete_collection(processing_id: str):
    client.delete_collection(f"collection_{processing_id}")

def collection_stats(processing_id: str):
    collection = client.get_collection(f"collection_{processing_id}")
    return {
        'count': collection.count(),
        'metadata': collection.metadata
    }

# Database cleanup
def cleanup_expired_collections(retention_hours: int = 24):
    cutoff_time = datetime.now() - timedelta(hours=retention_hours)
    
    for collection in client.list_collections():
        # Check creation time from metadata
        if collection.metadata.get('created_at'):
            created_at = datetime.fromisoformat(collection.metadata['created_at'])
            if created_at < cutoff_time:
                client.delete_collection(collection.name)
```

#### **FAISS Maintenance**
```python
# Index management
def list_faiss_indexes():
    faiss_dir = Path("backend/storage/.faiss")
    return [f.stem for f in faiss_dir.glob("*.index")]

def delete_faiss_index(processing_id: str):
    faiss_dir = Path("backend/storage/.faiss")
    
    # Remove index file
    index_file = faiss_dir / f"{processing_id}.index"
    if index_file.exists():
        index_file.unlink()
    
    # Remove metadata
    metadata_file = faiss_dir / f"{processing_id}.metadata.json"
    if metadata_file.exists():
        metadata_file.unlink()
    
    # Remove documents
    documents_file = faiss_dir / f"{processing_id}.documents.json"
    if documents_file.exists():
        documents_file.unlink()

def faiss_index_stats(processing_id: str):
    index = faiss.read_index(f"backend/storage/.faiss/{processing_id}.index")
    
    return {
        'total_vectors': index.ntotal,
        'dimension': index.d,
        'index_type': type(index).__name__,
        'is_trained': index.is_trained
    }
```

### 🔒 Data Security & Privacy

#### **Data Encryption**
```python
# Future enhancement: Encrypt embeddings at rest
def encrypt_embeddings(embeddings: np.ndarray, key: bytes) -> bytes:
    from cryptography.fernet import Fernet
    cipher = Fernet(key)
    
    # Serialize and encrypt
    embeddings_bytes = embeddings.tobytes()
    encrypted_data = cipher.encrypt(embeddings_bytes)
    
    return encrypted_data
```

#### **Access Control**
```python
# Future enhancement: Collection-level access control
collection_permissions = {
    "collection_uuid": {
        "owner": "user_id",
        "readers": ["user_id_1", "user_id_2"],
        "created_at": "2025-09-29T14:30:00Z",
        "expires_at": "2025-09-30T14:30:00Z"
    }
}
```

### 📊 Storage Size Estimation

#### **Size Calculation Formula**
```python
def estimate_storage_size(num_chunks: int, avg_text_length: int, 
                         vector_dimension: int = 384) -> dict:
    """Estimate storage requirements"""
    
    # Text storage (UTF-8)
    text_size = num_chunks * avg_text_length * 1.2  # 20% overhead
    
    # Vector storage (float32)
    vector_size = num_chunks * vector_dimension * 4  # 4 bytes per float
    
    # Metadata storage (JSON)
    metadata_size = num_chunks * 500  # ~500 bytes per metadata record
    
    # Index overhead
    index_overhead = vector_size * 0.3  # ~30% overhead for index
    
    total_size = text_size + vector_size + metadata_size + index_overhead
    
    return {
        'text_mb': text_size / 1024 / 1024,
        'vectors_mb': vector_size / 1024 / 1024, 
        'metadata_mb': metadata_size / 1024 / 1024,
        'index_mb': index_overhead / 1024 / 1024,
        'total_mb': total_size / 1024 / 1024
    }

# Example calculation
storage_estimate = estimate_storage_size(
    num_chunks=1000,
    avg_text_length=300,
    vector_dimension=384
)
print(f"Estimated storage: {storage_estimate['total_mb']:.2f} MB")
```

This database schema documentation provides complete understanding of how CSV Chunker Pro stores and retrieves vector embeddings using both ChromaDB and FAISS systems.

---