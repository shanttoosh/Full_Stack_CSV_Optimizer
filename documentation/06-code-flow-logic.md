# 6. Code Flow & Logic

### 🎯 User Journey Overview

The complete user journey from file upload to chunk retrieval follows this path:

```
1. User Opens Frontend → 2. Selects Layer → 3. Uploads CSV → 4. Starts Processing
                                                                      ↓
8. Searches Data ← 7. Downloads Files ← 6. Views Progress ← 5. Real-time Updates
```

### 🔄 Complete Data Flow Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │  FastAPI Routes │    │ Pipeline Service│
│                 │    │                 │    │                 │
│ 1. File Upload  │───▶│ 2. Layer API    │───▶│ 3. Orchestrate  │
│ 9. Display      │◀───│ 8. Response     │◀───│ 7. Results      │
│    Results      │    │    Builder      │    │    Collection   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       │                       │
         │                       │                       ▼
         │               ┌─────────────────┐    ┌─────────────────┐
         │               │ File Handler    │    │ Core Processing │
         │               │                 │    │                 │
         │               │ 4. Save File    │    │ 5. Preprocess   │
         │               │ 6. Create       │    │ 6. Chunk        │
         └───────────────│    Downloads    │◀───│ 7. Embed        │
                         └─────────────────┘    │ 8. Store        │
                                               └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │ Vector Database │
                                               │                 │
                                               │ • ChromaDB      │
                                               │ • FAISS         │
                                               │ • Metadata      │
                                               └─────────────────┘
```

### 🚀 Step-by-Step Processing Flow

#### **Phase 1: Frontend Initialization**
```javascript
// 1. Page Load
window.addEventListener('DOMContentLoaded', initializeApp);

function initializeApp() {
    // Initialize API client
    apiClient = new APIClient('http://localhost:8000');
    
    // Setup event listeners
    setupFileUpload();
    setupLayerSelection();
    setupProcessingControls();
    
    // Check backend health
    apiClient.checkHealth();
}
```

#### **Phase 2: File Upload & Validation**
```javascript
// 2. User selects/drops CSV file
function handleFileUpload(event) {
    const file = event.target.files[0] || event.dataTransfer.files[0];
    
    // Validate file
    if (!validateCSVFile(file)) {
        showError("Invalid file type or size");
        return;
    }
    
    // Convert to base64 for API transmission
    const base64Data = await readFileAsBase64(file);
    
    // Store for processing
    currentFile = { data: base64Data, name: file.name, size: file.size };
}
```

#### **Phase 3: Layer Selection & Configuration**
```javascript
// 3. User selects processing layer (Fast/Config/Deep)
function selectLayer(layerNumber) {
    currentLayer = layerNumber;
    
    // Show/hide configuration sections
    showConfigurationSections(layerNumber);
    
    // Load default settings
    loadLayerDefaults(layerNumber);
}
```

#### **Phase 4: Processing Initiation**
```javascript
// 4. User clicks "Start Processing"
async function startProcessing() {
    // Health check
    await apiClient.checkHealth();
    
    // Start dynamic step-by-step processing
    await processDynamicStepByStep(currentFile);
}

async function processDynamicStepByStep(file) {
    // Step 1: Preprocessing
    startStepTimer('step-preprocess', 'Preprocessing');
    const preprocessResult = await apiClient.processStepPreprocessing(file);
    stopStepTimer('step-preprocess', 'Preprocessing');
    
    // Step 2: Chunking
    startStepTimer('step-chunking', 'Chunking');
    const chunkingResult = await apiClient.processStepChunking(file);
    stopStepTimer('step-chunking', 'Chunking');
    
    // Step 3: Embedding
    startStepTimer('step-embedding', 'Embedding');
    const embeddingResult = await apiClient.processStepEmbedding(file);
    stopStepTimer('step-embedding', 'Embedding');
    
    // Step 4: Complete Processing (Storing + Setup)
    startStepTimer('step-storage', 'Storing');
    const fullResult = await apiClient.processLayer1(file);
    stopStepTimer('step-storage', 'Storing');
    
    // Handle success
    handleRealProcessingSuccess(fullResult);
}
```

### 🔧 Backend API Flow

#### **Phase 1: Request Reception**
```python
# FastAPI route handler
@router.post("/layer1/process")
async def process_layer1(request: LayerRequest) -> ProcessingResponse:
    try:
        # 1. Validate request data
        validate_csv_data(request.csv_data)
        
        # 2. Get layer defaults
        config = get_layer_defaults("fast")
        
        # 3. Call pipeline
        result = await pipeline.run_complete_pipeline(
            csv_data=request.csv_data,
            filename=request.filename,
            config=config
        )
        
        # 4. Build response
        return response_builder.build_processing_response(result)
        
    except Exception as e:
        return response_builder.build_error_response(str(e))
```

#### **Phase 2: Pipeline Orchestration**
```python
# Pipeline service coordination
async def run_complete_pipeline(csv_data: str, filename: str, config: dict):
    processing_id = generate_processing_id()
    
    try:
        # 1. Decode and load CSV
        df = decode_csv_data(csv_data)
        
        # 2. Run preprocessing
        processed_df, file_meta, numeric_meta = await _run_preprocessing(df, config)
        
        # 3. Run chunking
        chunking_result = await _run_chunking(processed_df, config)
        
        # 4. Run embedding
        embedding_result = await _run_embedding(chunking_result.chunks, config)
        
        # 5. Run storing
        storage_result = await _run_storing(embedding_result.embedded_chunks, config)
        
        # 6. Create download files
        file_paths = file_handler.create_download_files({
            'processing_id': processing_id,
            'chunks': chunking_result,
            'embeddings': embedding_result,
            'metadata': {'file_meta': file_meta, 'numeric_meta': numeric_meta}
        })
        
        # 7. Generate download links
        download_links = file_handler.generate_download_links(file_paths)
        
        return {
            'success': True,
            'processing_id': processing_id,
            'processing_summary': build_summary(chunking_result, embedding_result),
            'download_links': download_links,
            'search_endpoint': f'/api/v1/search/{processing_id}'
        }
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise
```

### 🔍 Core Processing Logic

#### **1. Preprocessing Flow**
```python
def preprocess_csv(df: pd.DataFrame, config: dict) -> tuple:
    # Data type detection
    type_info = validate_data_types(df)
    
    # Handle missing values
    if config.get('null_handling'):
        df = handle_missing_values(df, config['null_handling'])
    
    # Remove duplicates
    if config.get('remove_duplicates', True):
        df = remove_duplicates(df)
    
    # Type conversions
    if config.get('type_conversions'):
        df = apply_type_conversions(df, config['type_conversions'])
    
    # Generate metadata
    file_metadata = generate_file_metadata(df)
    numeric_metadata = generate_numeric_metadata(df)
    
    return df, file_metadata, numeric_metadata
```

#### **2. Chunking Flow**
```python
def chunk_dataframe(df: pd.DataFrame, method: str, **kwargs) -> ChunkingResult:
    # Create appropriate chunker
    chunker = create_chunker(method)
    
    # Validate parameters
    chunker.validate_params(**kwargs)
    
    # Perform chunking
    if method == 'semantic':
        result = chunker.chunk(df, n_clusters=kwargs.get('n_clusters', 5))
    elif method == 'fixed':
        result = chunker.chunk(df, chunk_size=kwargs.get('chunk_size', 100))
    elif method == 'recursive':
        result = chunker.chunk(df, chunk_size=kwargs.get('chunk_size', 1000))
    elif method == 'document_based':
        result = chunker.chunk(df, key_column=kwargs.get('key_column'))
    
    # Generate chunk metadata
    for i, chunk in enumerate(result.chunks):
        result.metadata.append({
            'chunk_id': f'{method}_chunk_{i:04d}',
            'method': method,
            'size': len(chunk),
            'source_rows': result.source_mapping[i]
        })
    
    return result
```

#### **3. Embedding Flow**
```python
def generate_chunk_embeddings(chunks: List[str], metadata: List[dict], 
                            model_name: str, batch_size: int) -> EmbeddingResult:
    # Load embedding model
    model = load_embedding_model(model_name)
    
    # Process in batches
    all_embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        
        # Generate embeddings
        batch_embeddings = model.encode(batch)
        all_embeddings.extend(batch_embeddings)
    
    # Validate embeddings
    quality_report = validate_embeddings(np.array(all_embeddings))
    
    # Combine with metadata
    embedded_chunks = []
    for i, (chunk, embedding) in enumerate(zip(chunks, all_embeddings)):
        embedded_chunks.append({
            'id': metadata[i]['chunk_id'],
            'embedding': embedding.tolist(),
            'document': chunk,
            'metadata': {
                **metadata[i],
                'embedding_model': model_name,
                'vector_dimension': len(embedding)
            }
        })
    
    return EmbeddingResult(
        embedded_chunks=embedded_chunks,
        model_used=model_name,
        vector_dimension=len(all_embeddings[0]),
        total_chunks=len(chunks),
        quality_report=quality_report
    )
```

#### **4. Storage Flow**
```python
def store_embeddings(embedded_chunks: List[dict], store_type: str, **kwargs):
    # Create vector store
    store = create_vector_store(store_type, **kwargs)
    
    # Prepare data for storage
    embeddings = [chunk['embedding'] for chunk in embedded_chunks]
    documents = [chunk['document'] for chunk in embedded_chunks]
    metadata = [chunk['metadata'] for chunk in embedded_chunks]
    ids = [chunk['id'] for chunk in embedded_chunks]
    
    # Store in database
    if store_type == 'chroma':
        store.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadata,
            ids=ids
        )
    elif store_type == 'faiss':
        # FAISS requires different approach
        store.add_vectors(np.array(embeddings), metadata, ids)
    
    # Persist to disk
    store.persist()
    
    return {
        'store_type': store_type,
        'total_vectors': len(embeddings),
        'dimension': len(embeddings[0]),
        'storage_path': kwargs.get('persist_directory')
    }
```

### 🔍 Search & Retrieval Flow

#### **Frontend Search Initiation**
```javascript
// User performs search
async function performExpandableSearch(processingId) {
    const query = document.getElementById('expandable-query-input').value;
    const topK = parseInt(document.getElementById('expandable-top-k').value);
    const metric = document.getElementById('expandable-similarity-metric').value;
    
    // Start retrieval timer
    startStepTimer('step-retrieval', 'Retrieval');
    
    try {
        // Call search API
        const results = await apiClient.searchChunks(processingId, query, {
            top_k: topK,
            similarity_metric: metric
        });
        
        // Stop timer and display results
        stopStepTimer('step-retrieval', 'Retrieval');
        displayExpandableSearchResults(results);
        
    } catch (error) {
        stopStepTimer('step-retrieval', 'Retrieval');
        showError('Search failed: ' + error.message);
    }
}
```

#### **Backend Search Processing**
```python
@router.post("/search/{processing_id}")
async def search_chunks(processing_id: str, request: SearchRequest):
    try:
        # 1. Load retriever for this processing session
        retriever = create_retriever(
            store_type="chroma",  # or "faiss"
            persist_directory=f"./backend/storage/.chroma",
            collection_name=f"collection_{processing_id}"
        )
        
        # 2. Perform search
        results = retriever.search(
            query=request.query,
            model_name=request.model_name,
            top_k=request.top_k,
            similarity_metric=request.similarity_metric
        )
        
        # 3. Format results
        formatted_results = []
        for i, (doc, score, metadata) in enumerate(zip(
            results['documents'][0],
            results['distances'][0],
            results['metadatas'][0]
        )):
            formatted_results.append({
                'rank': i + 1,
                'document': doc,
                'similarity_score': float(score),
                'chunk_id': metadata.get('chunk_id'),
                'chunk_method': metadata.get('chunk_method'),
                'source_file': metadata.get('source_file')
            })
        
        return {
            'success': True,
            'query': request.query,
            'total_results': len(formatted_results),
            'results': formatted_results,
            'search_metadata': {
                'model_used': request.model_name,
                'similarity_metric': request.similarity_metric,
                'top_k': request.top_k
            }
        }
        
    except Exception as e:
        return response_builder.build_error_response(f"Search failed: {e}")
```

### 📊 Real-time Progress Updates

#### **Frontend Timer Management**
```javascript
// Global timer storage
const activeTimers = new Map();

function startStepTimer(stepId, stepName) {
    const startTime = Date.now();
    
    // Update UI to show "Processing"
    updateStepStatus(stepId, 'active');
    updateStepStatusText(stepId, 'Processing');
    
    // Start live timer
    const intervalId = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        updateStepLiveTime(stepId, elapsed);
    }, 1000);
    
    // Store timer info
    activeTimers.set(stepId, {
        startTime,
        intervalId,
        stepName
    });
}

function stopStepTimer(stepId, stepName) {
    const timerInfo = activeTimers.get(stepId);
    if (!timerInfo) return;
    
    // Calculate final time
    const elapsed = Math.floor((Date.now() - timerInfo.startTime) / 1000);
    
    // Clear interval
    clearInterval(timerInfo.intervalId);
    
    // Update UI to show completion
    updateStepStatus(stepId, 'completed');
    updateStepCompletionTime(stepId, elapsed, stepName);
    
    // Remove from active timers
    activeTimers.delete(stepId);
}
```

### 🔄 Error Handling Flow

#### **Frontend Error Handling**
```javascript
function handleProcessingError(error) {
    console.error('Processing failed:', error);
    
    // Stop all active timers
    activeTimers.forEach((timerInfo, stepId) => {
        clearInterval(timerInfo.intervalId);
        updateStepStatus(stepId, 'error');
        updateStepStatusText(stepId, 'Failed');
    });
    
    // Show error message
    showErrorMessage(error.message || 'Processing failed');
    
    // Reset UI state
    resetProcessingState();
}
```

#### **Backend Error Handling**
```python
# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    
    return response_builder.build_error_response(
        error_message="Internal server error",
        error_code="500",
        details={"type": type(exc).__name__} if settings.DEBUG else None
    )

# Pipeline error handling
async def _run_chunking(df: pd.DataFrame, config: dict):
    try:
        return chunk_dataframe(df, **config['chunking'])
    except Exception as e:
        logger.error(f"Chunking failed: {e}")
        # Fallback to fixed chunking
        return chunk_dataframe(df, method='fixed', chunk_size=100)
```

### 🎯 Performance Optimization

#### **Async Processing**
```python
# Use asyncio for non-blocking operations
async def _run_embedding(chunks: List[str], config: dict):
    loop = asyncio.get_event_loop()
    
    # Run CPU-intensive embedding in thread pool
    embedding_result = await loop.run_in_executor(
        None,  # Use default thread pool
        functools.partial(
            generate_chunk_embeddings,
            chunks=chunks,
            chunk_metadata_list=[],
            **config['embedding']
        )
    )
    
    return embedding_result
```

#### **Memory Management**
```python
# Process large files in batches
def chunk_dataframe_batched(df: pd.DataFrame, batch_size: int = 1000):
    total_rows = len(df)
    all_chunks = []
    
    for start_idx in range(0, total_rows, batch_size):
        end_idx = min(start_idx + batch_size, total_rows)
        batch_df = df.iloc[start_idx:end_idx]
        
        # Process batch
        batch_chunks = process_batch(batch_df)
        all_chunks.extend(batch_chunks)
        
        # Clear memory
        del batch_df
        gc.collect()
    
    return all_chunks
```

This comprehensive flow documentation shows how data moves through the entire system from user interaction to final results, with real-time updates and robust error handling throughout the process.

---