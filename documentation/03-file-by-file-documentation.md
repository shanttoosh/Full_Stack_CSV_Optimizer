# 3. File-by-File Documentation

### 🌐 Frontend Files

#### **`frontend/index.html`** - Main Web Page
**Purpose**: The single HTML page that contains the entire user interface.

**Key Components**:
- **Document Structure**: HTML5 semantic markup with head and body sections
- **Layer Selection**: Radio buttons for choosing processing mode (Fast/Config/Deep)
- **File Upload**: Input field with drag-and-drop support and file validation
- **Processing Pipeline**: Visual progress indicator with 6 steps
- **Configuration Sections**: Collapsible panels for each processing layer
- **Action Buttons**: Reset, Save Config, and Start Processing controls

**Important Elements**:
```html
<!-- Layer Selection -->
<div class="layer-selector">
  <input type="radio" id="layer-1" name="layer" value="1" checked>
  <input type="radio" id="layer-2" name="layer" value="2">
  <input type="radio" id="layer-3" name="layer" value="3">
</div>

<!-- Processing Pipeline -->
<div class="processing-pipeline">
  <div class="process-step" id="step-upload">
    <div class="step-content">
      <div class="step-details">File Upload</div>
      <div class="step-right-container">
        <span class="step-status-text"></span>
        <span class="step-timing"></span>
        <div class="step-status">📁</div>
      </div>
    </div>
  </div>
  <!-- More steps... -->
</div>

<!-- Dynamic Sections (Created by JavaScript) -->
<div id="download-section"></div>
<div id="expandable-search-section"></div>
```

**Dependencies**: None (pure HTML5)
**Connects to**: `script.js` (functionality), `styles.css` (styling)

---

#### **`frontend/script.js`** - Core Application Logic
**Purpose**: Contains all JavaScript functionality for the frontend application.

**Major Functions & Classes**:

##### **APIClient Class**
```javascript
class APIClient {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }
  
  // Core API methods
  async checkHealth()              // Health check endpoint
  async processLayer1(file)        // Fast processing mode
  async processLayer2(file, config) // Config processing mode
  async processLayer3(file, config) // Deep processing mode
  async searchChunks(processingId, query, options) // Search functionality
}
```

##### **File Handling Functions**
```javascript
function handleFileUpload(event)     // Process file selection/drop
function validateCSVFile(file)       // Validate file type and size
function readFileAsBase64(file)      // Convert file to base64 for API
```

##### **Processing Pipeline Functions**
```javascript
function startProcessing()                    // Main processing orchestrator
function processDynamicStepByStep(file)      // Step-by-step processing
function handleRealProcessingSuccess(response) // Handle successful processing
function handleProcessingError(error)        // Handle processing errors
```

##### **UI Management Functions**
```javascript
function updateSidebarStats(stats)           // Update processing statistics
function showRealDownloadButtons(links)      // Create download interface
function enableExpandableSearchInterface(id) // Create search interface
function displayExpandableSearchResults(results) // Show search results
```

##### **Timer & Progress Functions**
```javascript
function startStepTimer(stepId, stepName)     // Start timing a processing step
function stopStepTimer(stepId, stepName)      // Stop timing and show completion
function updateStepLiveTime(stepId, seconds)  // Update live time display
function updateStepCompletionTime(stepId, seconds, stepName) // Final time display
```

##### **Search Functions**
```javascript
function performExpandableSearch(processingId) // Execute search query
function toggleSearchSection()                 // Expand/collapse search
function displayExpandableSearchResults(results) // Render search results
```

**Key Dependencies**:
- **Browser APIs**: Fetch API, FileReader API, DOM manipulation
- **ES6+ Features**: Classes, async/await, arrow functions, destructuring
- **No External Libraries**: Pure vanilla JavaScript

**Connects to**: `index.html` (DOM elements), Backend API (HTTP requests)

---

#### **`frontend/styles.css`** - User Interface Styling
**Purpose**: Complete CSS styling for the responsive user interface.

**Major CSS Sections**:

##### **Layout & Grid System**
```css
.app-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: min(320px, 25vw);
  background: #1a1a1a;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  background: #222;
  padding: clamp(10px, 2vw, 15px);
  overflow: hidden;
}
```

##### **Processing Pipeline Styles**
```css
.process-step {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin: 4px 0;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.step-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-height: 28px;
}

.step-right-container {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
  min-width: 150px;
  justify-content: flex-end;
}
```

##### **Interactive Elements**
```css
.layer-option:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3);
}

.upload-area.dragover {
  background: rgba(74, 144, 226, 0.1);
  border-color: #4a90e2;
  transform: scale(1.02);
}
```

##### **Responsive Design**
```css
@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
  }
}
```

**Features**:
- **CSS Grid & Flexbox**: Modern layout techniques
- **Custom Properties**: CSS variables for theming
- **Animations**: Smooth transitions and hover effects
- **Responsive Design**: Mobile-first approach with breakpoints
- **No External Frameworks**: Pure CSS without Bootstrap/Tailwind

**Connects to**: `index.html` (HTML elements)

---

### 🔧 Backend API Files

#### **`backend/api/main.py`** - FastAPI Application Entry Point
**Purpose**: Main FastAPI application setup with middleware, routes, and exception handling.

**Key Components**:
```python
# FastAPI App Creation
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Middleware Setup
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Route Inclusion
app.include_router(layer_router, prefix="/api/v1", tags=["Layer APIs"])
app.include_router(unified_router, prefix="/api/v1", tags=["Unified API"])
app.include_router(download_router, prefix="/api/v1", tags=["Downloads"])
app.include_router(search_router, prefix="/api/v1", tags=["Search"])
```

**Key Functions**:
- **`health_check()`**: Returns API health status
- **`api_info()`**: Returns API information and capabilities
- **`startup_event()`**: Initializes directories and background tasks
- **`shutdown_event()`**: Cleanup tasks on server shutdown

**Dependencies**: FastAPI, Uvicorn, config.settings, all route modules
**Connects to**: All route files, configuration, logging system

---

#### **`backend/api/models.py`** - Pydantic Data Models
**Purpose**: Defines data validation models for API requests and responses.

**Key Models**:
```python
class ProcessingRequest(BaseModel):
    csv_data: str  # Base64 encoded CSV data
    filename: str
    layer_mode: Optional[str] = "fast"

class ProcessingResponse(BaseModel):
    success: bool
    processing_id: str
    timestamp: str
    processing_summary: dict
    download_links: dict
    search_endpoint: str

class SearchRequest(BaseModel):
    query: str
    model_name: Optional[str] = "all-MiniLM-L6-v2"
    top_k: Optional[int] = 5
    similarity_metric: Optional[str] = "cosine"

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
```

**Features**:
- **Type Validation**: Automatic request/response validation
- **Documentation**: Auto-generated API docs from models
- **Serialization**: JSON serialization and deserialization

**Dependencies**: Pydantic, typing
**Connects to**: All API route files for request/response handling

---

### 🔧 Backend Routes

#### **`backend/api/routes/layer_routes.py`** - Layer Processing APIs
**Purpose**: Implements the three processing layers (Fast/Config/Deep modes).

**Key Endpoints**:
```python
@router.post("/layer1/process")  # Fast mode with optimized defaults
async def process_layer1(request: LayerRequest) -> ProcessingResponse

@router.post("/layer2/process")  # Config mode with customization
async def process_layer2(request: LayerRequest) -> ProcessingResponse

@router.post("/layer3/process")  # Deep mode with full control
async def process_layer3(request: LayerRequest) -> ProcessingResponse
```

**Processing Flow**:
1. **Request Validation**: Validate file data and parameters
2. **Pipeline Execution**: Call processing pipeline with layer-specific settings
3. **File Generation**: Create downloadable files (CSV, JSON, ZIP)
4. **Response Building**: Format response with download links and metadata

**Dependencies**: FastAPI, pipeline service, response builder
**Connects to**: Frontend API calls, processing pipeline, file handler

---

#### **`backend/api/routes/search_routes.py`** - Search & Retrieval APIs
**Purpose**: Handles semantic search queries against processed data.

**Key Endpoints**:
```python
@router.post("/search/{processing_id}")
async def search_chunks(
    processing_id: str,
    request: SearchRequest
) -> SearchResponse
```

**Search Process**:
1. **Vector Store Loading**: Load stored embeddings for processing ID
2. **Query Embedding**: Generate embedding for search query
3. **Similarity Search**: Find most similar chunks using specified metric
4. **Result Formatting**: Return ranked results with metadata

**Dependencies**: Core retrieval module, embedding service
**Connects to**: Vector databases (ChromaDB/FAISS), search interface

---

#### **`backend/api/routes/download_routes.py`** - File Download APIs
**Purpose**: Serves generated files for download with proper headers and expiration.

**Key Endpoints**:
```python
@router.get("/download/{filename}")
async def download_file(filename: str) -> FileResponse
```

**Download Features**:
- **Security**: Validates file existence and permissions
- **Headers**: Sets appropriate MIME types and download headers
- **Cleanup**: Tracks file access for automatic cleanup
- **Error Handling**: Returns 404 for missing/expired files

**Dependencies**: FastAPI FileResponse, file handler service
**Connects to**: Storage directories, download buttons in frontend

---

### 🔧 Backend Core Processing

#### **`backend/core/preprocessing.py`** - Data Preprocessing
**Purpose**: Cleans and prepares CSV data for chunking and embedding.

**Key Functions**:
```python
def preprocess_csv(df: pd.DataFrame, config: dict) -> tuple:
    # Data cleaning and validation
    
def validate_data_types(df: pd.DataFrame) -> dict:
    # Automatic type detection and validation
    
def handle_missing_values(df: pd.DataFrame, strategy: str) -> pd.DataFrame:
    # Handle null values with various strategies
    
def remove_duplicates(df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    # Remove duplicate rows based on specified columns
```

**Processing Steps**:
1. **Type Detection**: Automatically identify numeric, text, date columns
2. **Missing Value Handling**: Fill, drop, or interpolate missing values
3. **Duplicate Removal**: Remove exact or partial duplicates
4. **Text Cleaning**: Basic text preprocessing for text columns
5. **Validation**: Ensure data quality and consistency

**Dependencies**: Pandas, NumPy, data validation utilities
**Connects to**: Pipeline orchestrator, chunking module

---

#### **`backend/core/chunking.py`** - Text Chunking Algorithms
**Purpose**: Implements four different chunking strategies for optimal data splitting.

**Chunking Methods**:
```python
class FixedSizeChunker(BaseChunker):
    def chunk(self, df: pd.DataFrame, chunk_size: int) -> ChunkingResult
        # Split data into fixed-size chunks

class RecursiveChunker(BaseChunker):
    def chunk(self, df: pd.DataFrame, chunk_size: int) -> ChunkingResult
        # Intelligently split with context preservation

class SemanticChunker(BaseChunker):
    def chunk(self, df: pd.DataFrame, n_clusters: int) -> ChunkingResult
        # AI-powered clustering using KMeans

class DocumentChunker(BaseChunker):
    def chunk(self, df: pd.DataFrame, key_column: str) -> ChunkingResult
        # Group by document structure/key column
```

**Key Features**:
- **Strategy Pattern**: Pluggable chunking algorithms
- **Metadata Tracking**: Preserves chunk origin and relationships
- **Quality Metrics**: Evaluates chunk quality and distribution
- **Fallback Logic**: Automatic fallback if advanced methods fail

**Dependencies**: Scikit-learn, NLTK, LangChain text splitters
**Connects to**: Preprocessing output, embedding input

---

#### **`backend/core/embedding.py`** - Vector Embedding Generation
**Purpose**: Generates semantic vector embeddings using transformer models.

**Key Functions**:
```python
def generate_chunk_embeddings(
    chunks: List[str],
    chunk_metadata_list: List[dict],
    model_name: str = "all-MiniLM-L6-v2",
    batch_size: int = 32
) -> EmbeddingResult:
    # Generate embeddings for text chunks

def load_embedding_model(model_name: str):
    # Load and cache sentence transformer models

def validate_embeddings(embeddings: np.ndarray) -> dict:
    # Quality checks for generated embeddings
```

**Embedding Models**:
- **all-MiniLM-L6-v2**: Fast, 384-dimension embeddings
- **BAAI/bge-small-en-v1.5**: Higher quality, slower processing
- **Batch Processing**: Efficient GPU/CPU utilization
- **Quality Validation**: Checks for NaN, zero vectors, dimension consistency

**Dependencies**: Sentence Transformers, NumPy, model caching
**Connects to**: Chunking output, vector storage input

---

#### **`backend/core/storing.py`** - Vector Database Storage
**Purpose**: Stores embeddings in ChromaDB or FAISS vector databases.

**Key Functions**:
```python
def create_vector_store(store_type: str, **kwargs):
    # Factory method for vector store creation

def store_embeddings(embedded_chunks: List[dict], store_type: str, **kwargs):
    # Store embeddings with metadata in chosen database

class ChromaDBStore:
    def store(self, embeddings, metadata, collection_name)
    def search(self, query_embedding, top_k, metric)

class FAISSStore:
    def store(self, embeddings, metadata, index_path)
    def search(self, query_embedding, top_k, metric)
```

**Storage Options**:
- **ChromaDB**: Easy setup, good for development, persistent storage
- **FAISS**: High performance, production-ready, optimized search
- **Metadata Indexing**: Efficient metadata storage and retrieval
- **Similarity Metrics**: Cosine, dot product, Euclidean distance

**Dependencies**: ChromaDB, FAISS, NumPy for vector operations
**Connects to**: Embedding output, retrieval queries

---

#### **`backend/core/retrieval.py`** - Similarity Search & Ranking
**Purpose**: Performs semantic search against stored vector embeddings.

**Key Functions**:
```python
def create_retriever(store_type: str, **kwargs):
    # Factory method for retriever creation

def search_chunks(
    query: str,
    retriever,
    model_name: str,
    top_k: int = 5,
    similarity_metric: str = "cosine"
) -> dict:
    # Main search function

class BaseRetriever:
    def search(self, query, model_name, top_k, similarity_metric)
    def _embed_query(self, query, model_name)
    def _rank_results(self, results, metric)
```

**Search Features**:
- **Query Embedding**: Convert text queries to vectors
- **Similarity Calculation**: Multiple distance/similarity metrics
- **Result Ranking**: Sort and filter results by relevance
- **Metadata Enrichment**: Include chunk metadata in results

**Dependencies**: Vector stores, embedding models, similarity calculations
**Connects to**: Search API endpoints, vector databases

---

### 🔧 Backend Services

#### **`backend/services/pipeline.py`** - Processing Orchestration
**Purpose**: Coordinates the entire processing workflow from upload to storage.

**Key Functions**:
```python
async def run_complete_pipeline(
    csv_data: str,
    filename: str,
    config: dict
) -> dict:
    # Main pipeline orchestrator

async def _run_preprocessing(df: pd.DataFrame, config: dict) -> tuple:
    # Async preprocessing step

async def _run_chunking(df: pd.DataFrame, config: dict) -> ChunkingResult:
    # Async chunking step

async def _run_embedding(chunks: List[str], config: dict) -> EmbeddingResult:
    # Async embedding generation

async def _run_storing(embeddings: List[dict], config: dict) -> dict:
    # Async vector storage
```

**Pipeline Features**:
- **Async Execution**: Non-blocking processing using asyncio
- **Error Handling**: Comprehensive error catching and recovery
- **Progress Tracking**: Step-by-step timing and status updates
- **Resource Management**: Memory and CPU optimization
- **Fallback Logic**: Graceful degradation if components fail

**Dependencies**: All core modules, asyncio, concurrent.futures
**Connects to**: API routes, file handler, all processing modules

---

#### **`backend/services/file_handler.py`** - File Management
**Purpose**: Manages file uploads, downloads, temporary files, and cleanup.

**Key Functions**:
```python
def save_uploaded_file(file_data: bytes, filename: str) -> str:
    # Save uploaded files securely

def create_download_files(processing_result: dict) -> dict:
    # Generate downloadable files from processing results

def cleanup_expired_files():
    # Remove old files based on retention policy

def generate_download_links(file_paths: dict) -> dict:
    # Create secure download URLs
```

**File Management Features**:
- **Secure Storage**: Prevents directory traversal attacks
- **File Validation**: MIME type and size checking
- **Automatic Cleanup**: Configurable retention policies
- **Download Security**: Validates file access permissions
- **ZIP Creation**: Bundle multiple files for download

**Dependencies**: OS file operations, security utilities, ZIP library
**Connects to**: API routes, pipeline results, download endpoints

---

#### **`backend/services/response_builder.py`** - API Response Formatting
**Purpose**: Standardizes API responses with consistent formatting and error handling.

**Key Functions**:
```python
def build_processing_response(
    success: bool,
    processing_result: dict,
    processing_id: str,
    download_links: dict
) -> dict:
    # Format successful processing responses

def build_error_response(
    error_message: str,
    error_code: str = "500",
    details: dict = None
) -> dict:
    # Format error responses

def build_search_response(search_results: dict) -> dict:
    # Format search query responses

def build_health_response() -> dict:
    # Format health check responses
```

**Response Features**:
- **Consistent Structure**: All responses follow same format
- **Error Standardization**: Uniform error codes and messages
- **Metadata Inclusion**: Processing statistics and timing
- **URL Generation**: Automatic download link creation

**Dependencies**: UUID generation, datetime utilities
**Connects to**: All API routes, file handler

---

### 🔧 Backend Utilities

#### **`backend/utils/helpers.py`** - Helper Functions
**Purpose**: Common utility functions used across the application.

**Key Functions**:
```python
def get_layer_defaults(layer_mode: str) -> dict:
    # Load default configuration for processing layers

def validate_file_size(file_size: int, max_size: int) -> bool:
    # Validate uploaded file size

def generate_processing_id() -> str:
    # Generate unique identifiers for processing sessions

def format_processing_time(seconds: float) -> str:
    # Format time duration for display
```

**Dependencies**: Settings configuration, UUID, datetime
**Connects to**: Pipeline, API routes, configuration system

---

#### **`backend/utils/validators.py`** - Data Validation
**Purpose**: Validates data integrity and format throughout the application.

**Key Functions**:
```python
def validate_csv_data(csv_data: str) -> bool:
    # Validate CSV file format and content

def validate_processing_config(config: dict, layer: str) -> dict:
    # Validate and sanitize processing configuration

def validate_search_parameters(query: str, top_k: int, metric: str) -> bool:
    # Validate search query parameters
```

**Dependencies**: Pandas for CSV validation, JSON schema validation
**Connects to**: API routes, pipeline, data processing modules

---

#### **`backend/utils/base_chunker.py`** - Abstract Chunking Base
**Purpose**: Provides base class and interface for all chunking algorithms.

**Key Components**:
```python
class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, df: pd.DataFrame, **kwargs) -> ChunkingResult:
        # Abstract method for chunking implementation
    
    def validate_params(self, **kwargs) -> bool:
        # Common parameter validation
    
    def create_metadata(self, chunk_id: str, **kwargs) -> dict:
        # Generate chunk metadata
```

**Dependencies**: ABC (Abstract Base Classes), dataclasses
**Connects to**: All chunking implementations in core/chunking.py

---

### ⚙️ Configuration Files

#### **`config/settings.py`** - Application Configuration
**Purpose**: Central configuration management with environment variable support.

**Key Configuration Sections**:
```python
class Settings:
    # API Configuration
    APP_NAME: str = "CSV Chunking Optimizer Pro API"
    VERSION: str = "1.0.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # File Configuration
    MAX_FILE_SIZE_MB: int = 100
    ALLOWED_FILE_EXTENSIONS: list = [".csv"]
    
    # Processing Defaults
    LAYER_1_DEFAULTS = {"chunking": {"method": "semantic", "n_clusters": 5}}
    LAYER_2_DEFAULTS = {"chunking": {"method": "semantic", "n_clusters": 5}}
    LAYER_3_DEFAULTS = {"chunking": {"method": "document_based"}}
    
    # Storage Paths
    TEMP_FILES_DIR: Path = BASE_DIR / "backend" / "storage" / "temp_files"
    DOWNLOADS_DIR: Path = BASE_DIR / "backend" / "storage" / "downloads"
```

**Dependencies**: OS environment variables, pathlib
**Connects to**: All backend modules for configuration

---

#### **`config/logging.py`** - Logging Configuration
**Purpose**: Sets up application-wide logging with appropriate formatting and levels.

**Key Functions**:
```python
def setup_logging() -> logging.Logger:
    # Configure application logging

def create_file_handler(log_file: str) -> logging.FileHandler:
    # Set up file-based logging

def create_console_handler() -> logging.StreamHandler:
    # Set up console logging
```

**Logging Features**:
- **Multiple Handlers**: Console and file logging
- **Structured Format**: Timestamp, level, module, message
- **Rotation**: Automatic log file rotation
- **Level Configuration**: Debug/Info/Warning/Error levels

**Dependencies**: Python logging module, file system
**Connects to**: All modules for error and debug logging

---

### 🚀 Utility Scripts

#### **`scripts/start_server.py`** - Backend Server Launcher
**Purpose**: Starts the FastAPI backend server with proper configuration.

**Key Functions**:
```python
def start_backend_server():
    # Launch FastAPI with Uvicorn
    uvicorn.run(
        "backend.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
```

#### **`scripts/start_frontend.py`** - Frontend Server Launcher
**Purpose**: Serves frontend files using Python's built-in HTTP server.

#### **`scripts/start_full_stack.py`** - Complete Application Launcher
**Purpose**: Starts both backend and frontend servers simultaneously.

#### **`scripts/cleanup.py`** - File Cleanup Utility
**Purpose**: Removes expired files and cleans storage directories.

---

### 📄 Project Configuration Files

#### **`requirements.txt`** - Python Dependencies
**Purpose**: Lists all Python packages required to run the application.

**Key Dependencies**:
```
# Core Data Processing
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0

# Text Processing & NLP
sentence-transformers>=2.2.2
langchain>=0.1.0
nltk>=3.8

# Vector Databases
chromadb>=0.4.0
faiss-cpu>=1.7.4

# FastAPI & Web Framework
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.4.0
```

#### **`README.md`** - Basic Project Information
**Purpose**: Provides basic setup and usage instructions for the project.

---