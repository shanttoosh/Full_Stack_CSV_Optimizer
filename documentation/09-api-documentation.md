# 9. API Documentation

### 🌐 API Overview

CSV Chunker Pro provides a comprehensive REST API built with FastAPI, offering multiple endpoints for different use cases:

- **Layer APIs**: Three processing layers (Fast/Config/Deep) for UI integration
- **Unified API**: Single endpoint for enterprise integration
- **Search API**: Semantic search functionality
- **Download API**: File download endpoints
- **Utility APIs**: Health check and system information

**Base URL**: `http://localhost:8000`
**API Documentation**: `http://localhost:8000/api/docs` (Swagger UI)
**Alternative Docs**: `http://localhost:8000/api/redoc` (ReDoc)

### 📋 API Endpoint Summary

| **Category** | **Endpoint** | **Method** | **Purpose** |
|--------------|--------------|------------|-------------|
| **Health** | `/api/v1/health` | GET | Check API status |
| **Info** | `/api/v1/info` | GET | Get API information |
| **Layer 1** | `/api/v1/layer1/process` | POST | Fast processing mode |
| **Layer 2** | `/api/v1/layer2/process` | POST | Config processing mode |
| **Layer 3** | `/api/v1/layer3/process` | POST | Deep processing mode |
| **Unified** | `/api/v1/process-csv` | POST | Enterprise endpoint |
| **Search** | `/api/v1/search/{processing_id}` | POST | Semantic search |
| **Download** | `/api/v1/download/{filename}` | GET | File download |

### 🔍 Detailed API Endpoints

#### **Health Check API**

##### **GET `/api/v1/health`**
Check the health status of the API server.

**Parameters**: None

**Response Format**:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-29T14:30:00.123456Z",
  "version": "1.0.0",
  "uptime_seconds": 3600.5,
  "dependencies": {
    "database": "healthy",
    "storage": "healthy",
    "models": "loaded"
  }
}
```

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/health" \
  -H "Accept: application/json"
```

**Example Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-29T14:30:00.123456Z",
  "version": "1.0.0",
  "uptime_seconds": 3600.5
}
```

---

#### **API Information**

##### **GET `/api/v1/info`**
Get comprehensive API information and capabilities.

**Parameters**: None

**Response Format**:
```json
{
  "app_name": "CSV Chunking Optimizer Pro API",
  "version": "1.0.0",
  "description": "Complete CSV processing, chunking, embedding, and retrieval API",
  "available_endpoints": ["/api/v1/layer1/process", "..."],
  "supported_file_types": [".csv"],
  "max_file_size_mb": 100,
  "available_models": ["all-MiniLM-L6-v2", "BAAI/bge-small-en-v1.5"],
  "chunking_methods": ["fixed", "recursive", "semantic", "document_based"],
  "storage_types": ["chroma", "faiss"],
  "similarity_metrics": ["cosine", "dot", "euclidean"]
}
```

---

#### **Layer 1 API - Fast Processing**

##### **POST `/api/v1/layer1/process`**
Process CSV files using optimized defaults for fast processing.

**Request Body**:
```json
{
  "csv_data": "base64_encoded_csv_content",
  "filename": "data.csv"
}
```

**Parameters**:
- **`csv_data`** (string, required): Base64 encoded CSV file content
- **`filename`** (string, required): Original filename with .csv extension

**Default Configuration**:
```json
{
  "preprocessing": {
    "remove_duplicates": true,
    "text_processing": "skip"
  },
  "chunking": {
    "method": "semantic",
    "n_clusters": 5
  },
  "embedding": {
    "model": "all-MiniLM-L6-v2",
    "batch_size": 32
  },
  "storage": {
    "type": "chroma",
    "similarity_metric": "cosine"
  }
}
```

**Response Format**:
```json
{
  "success": true,
  "processing_id": "uuid-string",
  "timestamp": "2025-09-29T14:30:00.123456Z",
  "processing_summary": {
    "layer_mode": "fast",
    "processing_time_seconds": 15.43,
    "input_data": {
      "total_rows": 1000,
      "total_columns": 5,
      "file_size_bytes": 102400
    },
    "chunking_results": {
      "method": "semantic",
      "total_chunks": 25,
      "average_chunk_size": 40
    },
    "embedding_results": {
      "model_used": "all-MiniLM-L6-v2",
      "vector_dimension": 384,
      "total_embeddings": 25
    },
    "storage_results": {
      "store_type": "chroma",
      "collection_name": "collection_uuid-string"
    }
  },
  "download_links": {
    "chunks_csv": {
      "url": "/api/v1/download/chunks_uuid.csv",
      "filename": "chunks_data.csv",
      "size_bytes": 145230,
      "expires_at": "2025-09-30T14:30:00.123456Z"
    },
    "embeddings_json": {
      "url": "/api/v1/download/embeddings_uuid.json",
      "filename": "embeddings_data.json",
      "size_bytes": 2341567,
      "expires_at": "2025-09-30T14:30:00.123456Z"
    },
    "metadata_json": {
      "url": "/api/v1/download/metadata_uuid.json",
      "filename": "metadata.json",
      "size_bytes": 8945,
      "expires_at": "2025-09-30T14:30:00.123456Z"
    },
    "results_zip": {
      "url": "/api/v1/download/results_uuid.zip",
      "filename": "all_results.zip",
      "size_bytes": 2495742,
      "expires_at": "2025-09-30T14:30:00.123456Z"
    }
  },
  "search_endpoint": "/api/v1/search/uuid-string",
  "message": "Processing completed successfully"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/layer1/process" \
  -H "Content-Type: application/json" \
  -d '{
    "csv_data": "bmFtZSxhZ2UKSm9obiwyNQpKYW5lLDMw",
    "filename": "sample.csv"
  }'
```

---

#### **Layer 2 API - Config Processing**

##### **POST `/api/v1/layer2/process`**
Process CSV files with customizable configuration options.

**Request Body**:
```json
{
  "csv_data": "base64_encoded_csv_content",
  "filename": "data.csv",
  "chunking_method": "semantic",
  "n_clusters": 8,
  "embedding_model": "all-MiniLM-L6-v2",
  "batch_size": 64,
  "similarity_metric": "cosine"
}
```

**Parameters**:
- **`csv_data`** (string, required): Base64 encoded CSV content
- **`filename`** (string, required): Original filename
- **`chunking_method`** (string, optional): "fixed", "recursive", "semantic", "document_based"
- **`n_clusters`** (integer, optional): Number of clusters for semantic chunking (default: 5)
- **`chunk_size`** (integer, optional): Size for fixed/recursive chunking (default: 100)
- **`embedding_model`** (string, optional): Model name (default: "all-MiniLM-L6-v2")
- **`batch_size`** (integer, optional): Batch size for embedding (default: 32)
- **`similarity_metric`** (string, optional): "cosine", "dot", "euclidean" (default: "cosine")

**Response**: Same format as Layer 1 API

---

#### **Layer 3 API - Deep Processing**

##### **POST `/api/v1/layer3/process`**
Process CSV files with full control over all processing parameters.

**Request Body**:
```json
{
  "csv_data": "base64_encoded_csv_content",
  "filename": "data.csv",
  "preprocessing": {
    "type_conversions": {"age": "numeric", "date": "datetime"},
    "null_handling": {"column1": "mean", "column2": "drop"},
    "remove_duplicates": true,
    "remove_stopwords": false,
    "text_processing": "basic"
  },
  "chunking": {
    "method": "document_based",
    "key_column": "id",
    "token_limit": 2000,
    "overlap": 100
  },
  "embedding": {
    "model": "BAAI/bge-small-en-v1.5",
    "batch_size": 64,
    "normalize": true
  },
  "storage": {
    "type": "faiss",
    "similarity_metric": "cosine",
    "index_type": "flat"
  }
}
```

**Parameters**:
- **`csv_data`** (string, required): Base64 encoded CSV content
- **`filename`** (string, required): Original filename
- **`preprocessing`** (object, optional): Preprocessing configuration
  - **`type_conversions`**: Column type conversions
  - **`null_handling`**: Missing value handling strategies
  - **`remove_duplicates`**: Remove duplicate rows
  - **`text_processing`**: Text cleaning level
- **`chunking`** (object, optional): Chunking configuration
  - **`method`**: Chunking algorithm
  - **`key_column`**: Primary key column for document-based chunking
  - **`token_limit`**: Maximum tokens per chunk
  - **`overlap`**: Overlap between chunks
- **`embedding`** (object, optional): Embedding configuration
  - **`model`**: Sentence transformer model name
  - **`batch_size`**: Processing batch size
  - **`normalize`**: Normalize embeddings
- **`storage`** (object, optional): Storage configuration
  - **`type`**: Vector database type
  - **`similarity_metric`**: Distance/similarity metric
  - **`index_type`**: FAISS index type

**Response**: Same format as Layer 1 API

---

#### **Unified API - Enterprise**

##### **POST `/api/v1/process-csv`**
Single endpoint for enterprise integration with automatic layer selection.

**Request Body**:
```json
{
  "csv_data": "base64_encoded_csv_content",
  "filename": "data.csv",
  "layer_mode": "deep",
  "chunking": {
    "method": "semantic",
    "n_clusters": 5
  },
  "embedding": {
    "model": "all-MiniLM-L6-v2",
    "batch_size": 32
  },
  "storage": {
    "type": "chroma",
    "similarity_metric": "cosine"
  }
}
```

**Parameters**:
- **`csv_data`** (string, required): Base64 encoded CSV content
- **`filename`** (string, required): Original filename
- **`layer_mode`** (string, optional): "fast", "config", "deep" (default: "fast")
- **`chunking`** (object, optional): Chunking parameters
- **`embedding`** (object, optional): Embedding parameters
- **`storage`** (object, optional): Storage parameters

**Response**: Same format as Layer APIs

---

#### **Search API**

##### **POST `/api/v1/search/{processing_id}`**
Perform semantic search against processed data.

**Path Parameters**:
- **`processing_id`** (string, required): Processing session ID from processing response

**Request Body**:
```json
{
  "query": "customer information and demographics",
  "model_name": "all-MiniLM-L6-v2",
  "top_k": 5,
  "similarity_metric": "cosine",
  "threshold": 0.7
}
```

**Parameters**:
- **`query`** (string, required): Natural language search query
- **`model_name`** (string, optional): Embedding model for query (default: "all-MiniLM-L6-v2")
- **`top_k`** (integer, optional): Number of results to return (default: 5, max: 50)
- **`similarity_metric`** (string, optional): "cosine", "dot", "euclidean" (default: "cosine")
- **`threshold`** (float, optional): Minimum similarity score (default: 0.0)

**Response Format**:
```json
{
  "success": true,
  "query": "customer information and demographics",
  "total_results": 5,
  "search_metadata": {
    "model_used": "all-MiniLM-L6-v2",
    "similarity_metric": "cosine",
    "top_k": 5,
    "processing_time_seconds": 0.234
  },
  "results": [
    {
      "rank": 1,
      "similarity_score": 0.892,
      "chunk_id": "semantic_chunk_0003",
      "document": "Customer ID: 12345, Name: John Doe, Age: 35, Location: New York...",
      "metadata": {
        "chunk_method": "semantic",
        "source_file": "customer_data.csv",
        "chunk_number": 3,
        "text_length": 284,
        "source_rows": [45, 46, 47, 48, 49]
      }
    }
  ]
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/search/uuid-123" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "customer demographics",
    "top_k": 3,
    "similarity_metric": "cosine"
  }'
```

---

#### **Download API**

##### **GET `/api/v1/download/{filename}`**
Download processed files.

**Path Parameters**:
- **`filename`** (string, required): Filename from download_links in processing response

**Query Parameters**:
- **`attachment`** (boolean, optional): Force download as attachment (default: true)

**Response**: Binary file content with appropriate headers

**Headers**:
```
Content-Type: application/octet-stream (or specific MIME type)
Content-Disposition: attachment; filename="filename.ext"
Content-Length: file_size_in_bytes
Cache-Control: no-cache
```

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/download/chunks_uuid.csv" \
  -H "Accept: application/octet-stream" \
  --output "downloaded_chunks.csv"
```

### 🔧 Error Response Format

All API endpoints use a consistent error response format:

```json
{
  "success": false,
  "error": {
    "code": "PROCESSING_FAILED",
    "message": "Chunking algorithm failed to process the data",
    "details": {
      "error_type": "ValueError",
      "step": "chunking",
      "timestamp": "2025-09-29T14:30:00.123456Z"
    }
  },
  "request_id": "req-uuid-string"
}
```

**Common Error Codes**:
- **`INVALID_REQUEST`**: Malformed request or missing parameters
- **`FILE_TOO_LARGE`**: File exceeds size limit
- **`INVALID_FILE_TYPE`**: Non-CSV file uploaded
- **`PROCESSING_FAILED`**: Error during processing pipeline
- **`MODEL_UNAVAILABLE`**: Embedding model not found
- **`STORAGE_ERROR`**: Vector database issue
- **`NOT_FOUND`**: Processing ID or file not found
- **`EXPIRED`**: Download link expired
- **`RATE_LIMITED`**: Too many requests

### 📊 API Usage Examples

#### **Complete Processing Workflow**

```python
import requests
import base64
import json

# 1. Encode CSV file
with open('data.csv', 'rb') as f:
    csv_data = base64.b64encode(f.read()).decode()

# 2. Process with Layer 1 (Fast)
response = requests.post('http://localhost:8000/api/v1/layer1/process', 
    json={
        'csv_data': csv_data,
        'filename': 'data.csv'
    })

result = response.json()
print(f"Processing ID: {result['processing_id']}")

# 3. Download results
for file_type, file_info in result['download_links'].items():
    file_response = requests.get(f"http://localhost:8000{file_info['url']}")
    
    with open(f"downloaded_{file_info['filename']}", 'wb') as f:
        f.write(file_response.content)
    
    print(f"Downloaded: {file_info['filename']}")

# 4. Search the data
search_response = requests.post(
    f"http://localhost:8000/api/v1/search/{result['processing_id']}",
    json={
        'query': 'customer information',
        'top_k': 3
    })

search_results = search_response.json()
print(f"Found {search_results['total_results']} results")

for result in search_results['results']:
    print(f"Score: {result['similarity_score']:.3f}")
    print(f"Text: {result['document'][:100]}...")
```

#### **JavaScript Frontend Integration**

```javascript
class CSVChunkerAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }
    
    async processCSV(file, layer = 1) {
        // Convert file to base64
        const base64Data = await this.fileToBase64(file);
        
        // Process based on layer
        const endpoint = `${this.baseURL}/api/v1/layer${layer}/process`;
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                csv_data: base64Data,
                filename: file.name
            })
        });
        
        if (!response.ok) {
            throw new Error(`Processing failed: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    async searchData(processingId, query, options = {}) {
        const response = await fetch(
            `${this.baseURL}/api/v1/search/${processingId}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query,
                    top_k: options.topK || 5,
                    similarity_metric: options.metric || 'cosine'
                })
            }
        );
        
        return await response.json();
    }
    
    async fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }
}

// Usage
const api = new CSVChunkerAPI();

document.getElementById('file-input').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    
    try {
        const result = await api.processCSV(file, 1);
        console.log('Processing completed:', result.processing_id);
        
        // Search example
        const searchResults = await api.searchData(
            result.processing_id,
            'customer data',
            { topK: 5, metric: 'cosine' }
        );
        
        console.log('Search results:', searchResults.results);
        
    } catch (error) {
        console.error('Error:', error.message);
    }
});
```

### 🔒 Authentication & Security

**Current Version**: No authentication required (development mode)

**Production Considerations**:
- Add API key authentication
- Implement rate limiting per client
- Add request validation and sanitization
- Enable HTTPS/TLS encryption
- Add CORS restrictions for specific domains

**Security Headers**:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
```

### 📈 Rate Limiting

**Current Limits**:
- **Requests per minute**: 60 (configurable in settings)
- **File size limit**: 100MB (configurable)
- **Concurrent processing**: 5 sessions
- **Search requests**: 120 per minute

**Headers**:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

This comprehensive API documentation provides everything needed to integrate with CSV Chunker Pro programmatically.

---