# CSV Chunker Pro - Complete Project Documentation

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Project Structure](#2-project-structure)
3. [File-by-File Documentation](#3-file-by-file-documentation)
4. [Setup & Installation](#4-setup--installation)
5. [How to Run](#5-how-to-run)
6. [Code Flow & Logic](#6-code-flow--logic)
7. [Debugging Guide](#7-debugging-guide)
8. [Error Handling Matrix](#8-error-handling-matrix)
9. [API Documentation](#9-api-documentation)
10. [Database Schema](#10-database-schema)
11. [Frontend Components](#11-frontend-components)
12. [Configuration Files](#12-configuration-files)

---

## 1. Project Overview

### 🎯 Application Purpose
**CSV Chunker Pro** is a comprehensive web application that processes CSV files through an intelligent chunking, embedding, and retrieval pipeline. It transforms raw CSV data into searchable vector embeddings, enabling semantic search and data analysis capabilities.

**Key Capabilities:**
- **CSV Processing**: Upload and preprocess CSV files with data validation and cleaning
- **Smart Chunking**: Break down data using 4 different methods (Fixed, Recursive, Semantic, Document-based)
- **Vector Embeddings**: Generate semantic embeddings using state-of-the-art models
- **Vector Storage**: Store embeddings in ChromaDB or FAISS databases
- **Semantic Search**: Query data using natural language with similarity matching
- **File Downloads**: Export processed chunks, embeddings, and metadata
- **Real-time UI**: Dynamic progress tracking and live processing updates

### 🛠️ Technology Stack

#### **Frontend**
- **HTML5**: Modern semantic markup with responsive design
- **CSS3**: Flexbox layouts, CSS Grid, custom properties, animations
- **Vanilla JavaScript**: ES6+ features, async/await, fetch API, DOM manipulation
- **No Framework**: Pure JavaScript for maximum performance and minimal dependencies

#### **Backend**
- **Python 3.8+**: Core programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and serialization using Python type hints

#### **Data Processing**
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing and array operations
- **Scikit-learn**: Machine learning utilities (KMeans clustering)
- **NLTK**: Natural language processing toolkit
- **spaCy**: Advanced NLP library for text processing

#### **Text Processing & Embeddings**
- **Sentence Transformers**: Generate semantic embeddings
- **LangChain**: Text splitting and chunking utilities
- **Tiktoken**: Token counting for text processing
- **BeautifulSoup4**: HTML/XML parsing for text cleaning

#### **Vector Databases**
- **ChromaDB**: Easy-to-use vector database for development
- **FAISS**: High-performance similarity search and clustering
- **Vector Storage**: Persistent storage with metadata indexing

#### **File Handling**
- **Python-multipart**: Handle multipart form data and file uploads
- **aiofiles**: Asynchronous file operations
- **Base64**: Encode/decode binary data for API transmission

### 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │  FastAPI Backend│    │ Vector Databases│
│                 │    │                 │    │                 │
│ • File Upload   │────│ • API Routes    │────│ • ChromaDB      │
│ • Progress UI   │    │ • Processing    │    │ • FAISS         │
│ • Search Interface    │ • File Handler  │    │ • Metadata      │
│ • Download Links│    │ • Response Builder    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │ Processing Core │              │
         │              │                 │              │
         └──────────────│ • Preprocessing │──────────────┘
                        │ • Chunking      │
                        │ • Embedding     │
                        │ • Storing       │
                        │ • Retrieval     │
                        └─────────────────┘
```

#### **Architecture Layers**
1. **Presentation Layer**: HTML/CSS/JavaScript frontend with responsive UI
2. **API Layer**: FastAPI with RESTful endpoints and automatic documentation
3. **Service Layer**: Business logic orchestration and file management
4. **Core Processing Layer**: Specialized modules for each processing step
5. **Data Layer**: Vector databases and file storage systems

### ✨ Key Features

#### **🚀 Multi-Layer Processing**
- **Layer 1 (Fast Mode)**: Optimized defaults for quick processing
- **Layer 2 (Config Mode)**: Medium customization with user preferences
- **Layer 3 (Deep Mode)**: Full control over all processing parameters
- **Unified API**: Single endpoint for enterprise integration

#### **📊 Advanced Chunking Methods**
- **Fixed Size**: Split data into equal-sized chunks
- **Recursive**: Intelligent splitting with context preservation
- **Semantic**: AI-powered clustering using K-means algorithm
- **Document-based**: Chunk by document structure and key columns

#### **🧠 Embedding Models**
- **all-MiniLM-L6-v2**: Fast, lightweight model (384 dimensions)
- **BAAI/bge-small-en-v1.5**: Higher accuracy model for complex data
- **Batch Processing**: Configurable batch sizes for optimal performance

#### **🔍 Search Capabilities**
- **Semantic Search**: Natural language queries with context understanding
- **Multiple Metrics**: Cosine similarity, dot product, Euclidean distance
- **Top-K Results**: Configurable number of results with relevance scoring
- **Real-time Search**: Instant results with expandable interface

#### **📁 File Management**
- **Multiple Formats**: Export chunks (CSV), embeddings (JSON), metadata (JSON)
- **Batch Downloads**: Single ZIP file with all processed data
- **Automatic Cleanup**: Configurable file retention and cleanup
- **Secure Storage**: Temporary files with expiration timestamps

#### **🎨 User Interface**
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Progress**: Live updates with step-by-step timing
- **Dynamic Sections**: Expandable search interface and collapsible panels
- **Visual Feedback**: Progress bars, status indicators, and success/error states
- **No-Scroll Design**: Optimized layout that fits in viewport without scrolling

---

## 2. Project Structure

### 📁 Complete Directory Tree

```
csv-chunker-pro/
├── 📁 frontend/                    # Frontend web application
│   ├── index.html                  # Main HTML page
│   ├── script.js                   # Core JavaScript functionality
│   └── styles.css                  # CSS styling and layout
├── 📁 backend/                     # Python backend application
│   ├── __init__.py                 # Python package marker
│   ├── 📁 api/                     # FastAPI application layer
│   │   ├── __init__.py             # Package marker
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── models.py               # Pydantic data models
│   │   ├── 📁 dependencies/        # Dependency injection
│   │   │   └── __init__.py         # Package marker
│   │   ├── 📁 middleware/          # Custom middleware
│   │   │   └── __init__.py         # Package marker
│   │   └── 📁 routes/              # API endpoint definitions
│   │       ├── __init__.py         # Package marker
│   │       ├── layer_routes.py     # Layer 1/2/3 APIs
│   │       ├── unified_routes.py   # Single unified API
│   │       ├── download_routes.py  # File download endpoints
│   │       └── search_routes.py    # Search functionality
│   ├── 📁 core/                    # Core processing modules
│   │   ├── __init__.py             # Package marker
│   │   ├── preprocessing.py        # Data preprocessing
│   │   ├── chunking.py             # Text chunking algorithms
│   │   ├── embedding.py            # Vector embedding generation
│   │   ├── storing.py              # Vector database storage
│   │   └── retrieval.py            # Similarity search
│   ├── 📁 services/                # Business logic layer
│   │   ├── __init__.py             # Package marker
│   │   ├── pipeline.py             # Processing orchestration
│   │   ├── file_handler.py         # File management
│   │   └── response_builder.py     # API response formatting
│   ├── 📁 utils/                   # Utility functions
│   │   ├── __init__.py             # Package marker
│   │   ├── helpers.py              # Helper functions
│   │   ├── validators.py           # Data validation
│   │   └── base_chunker.py         # Base chunking class
│   └── 📁 storage/                 # File storage directories
│       ├── __init__.py             # Package marker
│       ├── 📁 downloads/           # Generated files storage
│       ├── 📁 temp_files/          # Temporary file storage
│       ├── 📁 .chroma/             # ChromaDB database (auto-created)
│       └── 📁 .faiss/              # FAISS database (auto-created)
├── 📁 config/                      # Configuration files
│   ├── __init__.py                 # Package marker
│   ├── settings.py                 # App configuration & defaults
│   └── logging.py                  # Logging configuration
├── 📁 scripts/                     # Utility scripts
│   ├── start_server.py             # Backend server launcher
│   ├── start_frontend.py           # Frontend server launcher
│   ├── start_full_stack.py         # Full application launcher
│   └── cleanup.py                  # File cleanup utility
├── 📁 logs/                        # Log files (auto-created)
│   └── app.log                     # Application logs
├── requirements.txt                # Python dependencies
├── README.md                       # Basic project information
├── DOCUMENTATION.md                # This comprehensive documentation
├── test_backend.py                 # Backend testing script (optional)
├── test_api.py                     # API testing script (optional)
└── test_complete_system.py         # Full system test (optional)
```

### 📂 Directory Explanations

#### **🌐 frontend/ - Web User Interface**
Contains the complete web application that users interact with:
- **Single Page Application**: No page reloads, dynamic content updates
- **Responsive Design**: Works on all screen sizes and devices
- **Real-time Updates**: Live progress tracking and status updates
- **File Management**: Upload interface and download buttons
- **Search Interface**: Expandable search section with results display

#### **🔧 backend/ - Python Server Application**
The core server application built with FastAPI:

##### **api/ - Web API Layer**
- **main.py**: FastAPI application setup, middleware, exception handling
- **models.py**: Data models for request/response validation
- **routes/**: API endpoints organized by functionality
  - **layer_routes.py**: Three processing layers (Fast/Config/Deep)
  - **unified_routes.py**: Single endpoint for enterprise integration
  - **download_routes.py**: File download and serving endpoints
  - **search_routes.py**: Search and retrieval endpoints

##### **core/ - Processing Engine**
Specialized modules for each step of the data processing pipeline:
- **preprocessing.py**: Data cleaning, validation, type conversion
- **chunking.py**: Four chunking algorithms implementation
- **embedding.py**: Vector embedding generation using AI models
- **storing.py**: Vector database operations (ChromaDB/FAISS)
- **retrieval.py**: Similarity search and ranking algorithms

##### **services/ - Business Logic**
High-level orchestration and management services:
- **pipeline.py**: Coordinates the entire processing workflow
- **file_handler.py**: Manages file uploads, downloads, and cleanup
- **response_builder.py**: Standardizes API response formatting

##### **utils/ - Helper Functions**
Common utilities used across the application:
- **helpers.py**: Configuration loading and general utilities
- **validators.py**: Data validation and error checking
- **base_chunker.py**: Abstract base class for chunking algorithms

##### **storage/ - Data Storage**
File and database storage locations:
- **downloads/**: Generated CSV, JSON, and ZIP files for user download
- **temp_files/**: Temporary files during processing
- **`.chroma/`**: ChromaDB vector database files (auto-created)
- **`.faiss/`**: FAISS index files (auto-created)

#### **⚙️ config/ - Configuration Management**
Application configuration and settings:
- **settings.py**: Central configuration with environment variables
- **logging.py**: Logging setup and formatting

#### **🚀 scripts/ - Utility Scripts**
Scripts for running and managing the application:
- **start_server.py**: Launches FastAPI backend server
- **start_frontend.py**: Serves frontend files with Python HTTP server
- **start_full_stack.py**: Starts both frontend and backend together
- **cleanup.py**: Removes old files and cleans storage directories

### 📊 Directory Size and Complexity

| Directory | Files | Purpose | Complexity |
|-----------|-------|---------|------------|
| `frontend/` | 3 | UI Layer | Medium |
| `backend/api/` | 6+ | API Layer | High |
| `backend/core/` | 5 | Processing | High |
| `backend/services/` | 3 | Business Logic | Medium |
| `backend/utils/` | 3 | Utilities | Low |
| `config/` | 2 | Configuration | Low |
| `scripts/` | 4 | Operations | Low |

### 🔄 Data Flow Between Directories

```
User Upload → frontend/ → backend/api/ → backend/services/ → backend/core/ → backend/storage/
                ↓              ↓              ↓              ↓              ↓
            UI Updates ← API Response ← File Handler ← Pipeline ← Vector DB
```

---

## 3. File-by-File Documentation

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

## 4. Setup & Installation

### 📋 Prerequisites

Before installing CSV Chunker Pro, ensure you have the following software installed:

#### **Required Software**
```bash
Python 3.8+                    # Core runtime (3.8, 3.9, 3.10, 3.11 supported)
pip                            # Python package manager (comes with Python)
```

#### **Optional but Recommended**
```bash
Git                            # For cloning the repository
Virtual Environment Tool       # venv, conda, or virtualenv
Text Editor/IDE                # VS Code, PyCharm, or similar
```

#### **System Requirements**
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: Minimum 4GB, Recommended 8GB+ (for large CSV files)
- **Storage**: 2GB free space (for dependencies and temporary files)
- **Internet**: Required for downloading models and dependencies

### 🚀 Installation Steps

#### **Step 1: Clone or Download Repository**

**Option A: Using Git (Recommended)**
```bash
# Clone the repository
git clone <repository-url>
cd csv-chunker-pro

# Or if you have the project folder already
cd path/to/csv-chunker-pro
```

**Option B: Download ZIP**
1. Download the project ZIP file
2. Extract to your desired location
3. Open terminal in the project folder

#### **Step 2: Create Virtual Environment (Recommended)**

**Using Python venv:**
```bash
# Create virtual environment
python -m venv chunker_env

# Activate virtual environment
# On Windows:
chunker_env\Scripts\activate

# On macOS/Linux:
source chunker_env/bin/activate

# Verify activation (should show virtual environment name)
which python  # Should point to virtual environment
```

**Using Conda:**
```bash
# Create conda environment
conda create -n chunker_env python=3.9

# Activate environment
conda activate chunker_env
```

#### **Step 3: Install Python Dependencies**

```bash
# Install all required packages
pip install -r requirements.txt

# This will install:
# - FastAPI and Uvicorn (web framework)
# - Pandas and NumPy (data processing)
# - Scikit-learn (machine learning)
# - Sentence Transformers (embeddings)
# - ChromaDB and FAISS (vector databases)
# - And many more dependencies...
```

**Installation Progress Indicator:**
```bash
# You should see output like:
Collecting pandas>=2.0.0
  Downloading pandas-2.1.0-cp39-cp39-win_amd64.whl (10.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 10.7/10.7 MB 5.2 MB/s eta 0:00:00
Installing collected packages: pandas, numpy, ...
Successfully installed pandas-2.1.0 numpy-1.24.3 ...
```

#### **Step 4: Download Required NLP Models**

```bash
# Download spaCy English model (required for text processing)
python -m spacy download en_core_web_sm

# This will download ~50MB of language models
# Output should show:
# ✔ Download and installation successful
```

#### **Step 5: Verify Installation**

```bash
# Test backend components
python test_backend.py

# Expected output:
# 🚀 Testing CSV Chunking Optimizer Pro Backend
# ✅ Preprocessing: Working
# ✅ Chunking: Working
# ✅ Embedding: Working
# ✅ Storing: Working
# ✅ Retrieval: Working
# 🎉 Backend testing completed!
```

### ⚙️ Environment Variables (Optional)

Create a `.env` file in the project root for custom configuration:

```bash
# .env file (optional)
HOST=127.0.0.1
PORT=8000
DEBUG=True
MAX_FILE_SIZE_MB=100
FILE_RETENTION_HOURS=24
RATE_LIMIT_PER_MINUTE=60
```

**Environment Variable Explanations:**
- **`HOST`**: Server bind address (default: 127.0.0.1)
- **`PORT`**: Server port number (default: 8000)
- **`DEBUG`**: Enable debug mode (default: False)
- **`MAX_FILE_SIZE_MB`**: Maximum upload size (default: 100MB)
- **`FILE_RETENTION_HOURS`**: How long to keep files (default: 24 hours)
- **`RATE_LIMIT_PER_MINUTE`**: API rate limiting (default: 60 requests/minute)

### 📁 Configuration Setup

#### **Automatic Directory Creation**
The application automatically creates required directories on first run:
```
backend/storage/
├── downloads/          # Generated files for download
├── temp_files/         # Temporary processing files
├── .chroma/           # ChromaDB database files
└── .faiss/            # FAISS index files
```

#### **Manual Configuration (Advanced)**

**Edit `config/settings.py` for advanced configuration:**
```python
# Modify default processing settings
LAYER_1_DEFAULTS = {
    "chunking": {
        "method": "semantic",        # Change default chunking method
        "n_clusters": 5             # Change default cluster count
    },
    "embedding": {
        "model": "all-MiniLM-L6-v2", # Change default embedding model
        "batch_size": 32            # Adjust batch size for performance
    }
}
```

### 🔧 Database Setup

#### **ChromaDB (Default - No Setup Required)**
- **Automatic**: Creates database on first use
- **Location**: `backend/storage/.chroma/`
- **Best for**: Development, small to medium datasets

#### **FAISS (Optional - For Performance)**
- **Automatic**: Creates indexes on first use
- **Location**: `backend/storage/.faiss/`
- **Best for**: Production, large datasets, high performance

#### **No External Database Required**
- Both vector databases are embedded and require no separate installation
- No PostgreSQL, MySQL, or MongoDB setup needed
- Everything runs locally

### 🧪 Installation Verification

#### **Quick Health Check**
```bash
# Start the backend server
python scripts/start_server.py

# In another terminal, test the API
curl http://localhost:8000/api/v1/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-09-29T...",
  "version": "1.0.0"
}
```

#### **Full System Test**
```bash
# Stop the server (Ctrl+C) and run complete test
python test_complete_system.py

# This tests:
# - Backend modules
# - API endpoints
# - File processing
# - Database operations
# - Frontend integration
```

### 🐛 Common Installation Issues

#### **Issue 1: Python Version Mismatch**
```bash
# Error: "Python 3.8+ required"
# Solution: Check your Python version
python --version

# If too old, install newer Python from python.org
# Then create new virtual environment with correct version
```

#### **Issue 2: pip Install Failures**
```bash
# Error: "Failed building wheel for X"
# Solution 1: Upgrade pip
python -m pip install --upgrade pip

# Solution 2: Install build tools
# On Windows:
pip install --upgrade setuptools wheel

# On macOS:
xcode-select --install

# On Linux (Ubuntu):
sudo apt-get install python3-dev build-essential
```

#### **Issue 3: spaCy Model Download Fails**
```bash
# Error: "Cannot download en_core_web_sm"
# Solution: Manual download
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0-py3-none-any.whl
```

#### **Issue 4: ChromaDB/FAISS Installation Issues**
```bash
# Error: Problems with vector databases
# Solution: Install individually to identify issue
pip install chromadb
pip install faiss-cpu

# If FAISS fails, try conda:
conda install -c conda-forge faiss-cpu
```

#### **Issue 5: Port Already in Use**
```bash
# Error: "Address already in use"
# Solution 1: Change port in .env file
PORT=8001

# Solution 2: Find and kill process using port
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# On macOS/Linux:
lsof -i :8000
kill -9 <process_id>
```

### ✅ Installation Success Checklist

- [ ] **Python 3.8+** installed and accessible
- [ ] **Virtual environment** created and activated  
- [ ] **All dependencies** installed via `pip install -r requirements.txt`
- [ ] **spaCy model** downloaded with `python -m spacy download en_core_web_sm`
- [ ] **Backend test** passes with `python test_backend.py`
- [ ] **API health check** responds correctly
- [ ] **Required directories** created automatically
- [ ] **Environment variables** configured (if needed)

### 🎉 Ready to Run!

Once all installation steps are complete, you're ready to run CSV Chunker Pro! Proceed to the next section for detailed instructions on how to start and use the application.

**Next Steps:**
1. **Start the application** (see "How to Run" section)
2. **Upload a CSV file** through the web interface
3. **Process and download** your chunked data
4. **Search and query** your processed data

---

## 5. How to Run

### 🚀 Quick Start (Recommended)

The easiest way to start CSV Chunker Pro is using the full-stack launcher:

```bash
# Start both backend and frontend together
python scripts/start_full_stack.py
```

**Expected Output:**
```bash
🚀 Starting CSV Chunker Pro - Full Stack
============================================================
🔧 Starting FastAPI backend...
🌐 Starting frontend server...

============================================================
✅ Full Stack Started Successfully!
🌐 Frontend: http://localhost:3000
🔧 Backend API: http://localhost:8000
📖 API Docs: http://localhost:8000/api/docs
============================================================

🎉 Your frontend is now DYNAMIC!
   - Connected to real FastAPI backend
   - Real CSV processing
   - Real file downloads
   - Real search functionality

🛑 Press Ctrl+C to stop both servers
```

### 🔧 Individual Server Commands

#### **Start Backend Server Only**
```bash
# Option 1: Using the script (recommended)
python scripts/start_server.py

# Option 2: Direct uvicorn command
uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload

# Option 3: Using Python module
python -m backend.api.main
```

**Backend Output:**
```bash
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Starting CSV Chunking Optimizer Pro API v1.0.0
INFO:     Server will run on 127.0.0.1:8000
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

#### **Start Frontend Server Only**
```bash
# Using the script
python scripts/start_frontend.py

# This serves the frontend/ directory on port 3000
```

**Frontend Output:**
```bash
🌐 Starting CSV Chunker Pro Frontend
Serving at http://localhost:3000
Press Ctrl+C to stop the server
```

### 🔌 Port Configuration

#### **Default Ports**
- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/api/docs`
- **Alternative API Docs**: `http://localhost:8000/api/redoc`

#### **Change Ports (if needed)**

**Method 1: Environment Variables**
```bash
# Create .env file
echo "PORT=8001" > .env

# Or set temporarily
export PORT=8001  # Linux/macOS
set PORT=8001     # Windows

python scripts/start_server.py
```

**Method 2: Direct Command**
```bash
# Backend on different port
uvicorn backend.api.main:app --host 127.0.0.1 --port 8001

# Frontend on different port (edit start_frontend.py)
# Change: server.serve_forever() to use different port
```

### 🏃‍♂️ Development vs Production Mode

#### **Development Mode (Default)**
```bash
# Features:
# - Auto-reload on file changes
# - Debug information
# - Detailed error messages
# - CORS enabled for localhost

python scripts/start_server.py
# or
uvicorn backend.api.main:app --reload --host 127.0.0.1 --port 8000
```

#### **Production Mode**
```bash
# Features:
# - No auto-reload
# - Optimized performance
# - Limited error details
# - Security hardening

# Single worker
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000

# Multiple workers (recommended for production)
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### ✅ Verification Steps

#### **Step 1: Check Backend Health**
```bash
# Test 1: Health endpoint
curl http://localhost:8000/api/v1/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2025-09-29T...",
  "version": "1.0.0",
  "uptime_seconds": 45.2
}

# Test 2: API info
curl http://localhost:8000/api/v1/info

# Expected response:
{
  "app_name": "CSV Chunking Optimizer Pro API",
  "version": "1.0.0",
  "available_endpoints": [...],
  "supported_file_types": [".csv"],
  "max_file_size_mb": 100
}
```

#### **Step 2: Check Frontend Access**
```bash
# Open in browser or test with curl
curl http://localhost:3000

# Expected: HTML page with CSV Chunker Pro interface
# Should see: Layer selection, file upload area, processing pipeline
```

#### **Step 3: Test API Documentation**
Visit in browser:
- **Swagger UI**: `http://localhost:8000/api/docs`
- **ReDoc**: `http://localhost:8000/api/redoc`

Should see interactive API documentation with all endpoints.

#### **Step 4: Verify File Processing**
```bash
# Test with a small CSV file
curl -X POST "http://localhost:8000/api/v1/layer1/process" \
  -H "Content-Type: application/json" \
  -d '{
    "csv_data": "bmFtZSxhZ2UKSm9obiwyNQpKYW5lLDMw",
    "filename": "test.csv"
  }'

# Expected: JSON response with processing_id and download_links
```

### 🔄 Server Management

#### **Starting Servers in Background**

**Linux/macOS:**
```bash
# Start backend in background
nohup python scripts/start_server.py > backend.log 2>&1 &

# Start frontend in background
nohup python scripts/start_frontend.py > frontend.log 2>&1 &

# Check running processes
ps aux | grep python
```

**Windows:**
```bash
# Start backend in background
start /B python scripts/start_server.py

# Start frontend in background  
start /B python scripts/start_frontend.py

# Check running processes
tasklist | findstr python
```

#### **Stopping Servers**

**Graceful Shutdown:**
```bash
# If running in foreground: Press Ctrl+C

# If running in background:
# Find process ID
ps aux | grep "start_server.py"  # Linux/macOS
tasklist | findstr python        # Windows

# Kill process
kill <process_id>        # Linux/macOS
taskkill /PID <id> /F   # Windows
```

#### **Automatic Restart on Failure**

**Using systemd (Linux):**
```bash
# Create service file: /etc/systemd/system/csv-chunker.service
[Unit]
Description=CSV Chunker Pro
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/csv-chunker-pro
ExecStart=/path/to/python scripts/start_full_stack.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable csv-chunker
sudo systemctl start csv-chunker
```

### 🌐 Network Access

#### **Local Access Only (Default)**
```bash
# Backend binds to 127.0.0.1 (localhost only)
# Frontend serves on localhost:3000
# Only accessible from same machine
```

#### **Network Access (LAN)**
```bash
# Backend: Change host to 0.0.0.0
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000

# Frontend: Modify start_frontend.py to bind to 0.0.0.0
# Access via: http://YOUR_IP:3000 and http://YOUR_IP:8000
```

#### **Firewall Configuration**
```bash
# Linux (ufw)
sudo ufw allow 8000
sudo ufw allow 3000

# Windows: Add inbound rules for ports 8000 and 3000
# macOS: System Preferences > Security & Privacy > Firewall
```

### 📊 Performance Monitoring

#### **Resource Usage**
```bash
# Monitor CPU and memory usage
top -p $(pgrep -f "start_server.py")  # Linux
Get-Process python | Where-Object {$_.ProcessName -eq "python"}  # Windows PowerShell
```

#### **API Performance**
```bash
# Test API response times
time curl http://localhost:8000/api/v1/health

# Load testing (install apache-bench)
ab -n 100 -c 10 http://localhost:8000/api/v1/health
```

### 🐛 Common Runtime Issues

#### **Issue 1: Port Already in Use**
```bash
# Error: "Address already in use"
# Solution: Kill process or change port

# Find process using port
lsof -i :8000                    # Linux/macOS
netstat -ano | findstr :8000     # Windows

# Kill process or change port in configuration
```

#### **Issue 2: Module Not Found**
```bash
# Error: "ModuleNotFoundError: No module named 'backend'"
# Solution: Run from project root directory

cd /path/to/csv-chunker-pro
python scripts/start_server.py
```

#### **Issue 3: Permission Denied**
```bash
# Error: "Permission denied" when creating directories
# Solution: Check directory permissions

chmod 755 backend/storage/  # Linux/macOS
# Or run with appropriate user permissions
```

#### **Issue 4: Frontend Can't Connect to Backend**
```bash
# Error: CORS errors in browser console
# Solution: Check backend is running and CORS settings

# Verify backend is running
curl http://localhost:8000/api/v1/health

# Check CORS settings in config/settings.py
CORS_ORIGINS = ["http://localhost:3000", "*"]
```

### 🎯 Quick Troubleshooting Commands

```bash
# Check if servers are running
curl http://localhost:8000/api/v1/health  # Backend
curl http://localhost:3000                # Frontend

# Check logs
tail -f logs/app.log                      # Application logs
tail -f backend.log                       # Backend logs (if backgrounded)

# Restart everything
pkill -f "python scripts"                 # Kill all Python scripts
python scripts/start_full_stack.py        # Restart full stack

# Test with minimal CSV
echo "name,age\nJohn,25" | base64        # Create test data
# Use this base64 string in API test
```

### ✅ Verification Checklist

After starting the application, verify:

- [ ] **Backend responds** to `http://localhost:8000/api/v1/health`
- [ ] **Frontend loads** at `http://localhost:3000`
- [ ] **API docs accessible** at `http://localhost:8000/api/docs`
- [ ] **File upload works** (drag & drop or click to select)
- [ ] **Processing completes** (progress bars update)
- [ ] **Downloads appear** after processing
- [ ] **Search functionality** works in expandable section
- [ ] **No CORS errors** in browser console
- [ ] **Logs show no errors** in `logs/app.log`

### 🎉 Ready to Use!

Once all verification steps pass, CSV Chunker Pro is ready for use! You can now:

1. **Upload CSV files** up to 100MB
2. **Choose processing layer** (Fast/Config/Deep)
3. **Monitor real-time progress** with live timing
4. **Download processed files** (chunks, embeddings, metadata)
5. **Search your data** using natural language queries
6. **View API documentation** for integration

**Access Points:**
- **Main Interface**: http://localhost:3000
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/api/v1/health

---

## 6. Code Flow & Logic

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

## 7. Debugging Guide

### 🔍 General Debugging Strategy

When encountering issues with CSV Chunker Pro, follow this systematic approach:

```
1. Identify the Layer → 2. Check Logs → 3. Verify Environment → 4. Test Components → 5. Isolate Issue
```

### 📂 Log File Locations

#### **Application Logs**
```bash
# Main application log
logs/app.log                    # Structured application logs

# Backend-specific logs (if running separately)
backend.log                     # Backend process output
frontend.log                    # Frontend server output

# System logs (Linux)
/var/log/syslog                # System-wide logs
journalctl -u csv-chunker      # Systemd service logs
```

#### **Log Viewing Commands**
```bash
# View recent logs
tail -f logs/app.log            # Follow real-time logs

# View specific number of lines
tail -n 100 logs/app.log        # Last 100 lines

# Search logs for errors
grep -i "error" logs/app.log    # Find error messages
grep -i "failed" logs/app.log   # Find failure messages

# View logs by timestamp
grep "2025-09-29" logs/app.log  # Logs from specific date
```

### 🖥️ Browser Console Debugging

#### **Opening Developer Tools**
```
Chrome/Edge: F12 or Ctrl+Shift+I
Firefox: F12 or Ctrl+Shift+K
Safari: Cmd+Option+I (after enabling Developer menu)
```

#### **Key Console Areas to Check**

**1. Console Tab - JavaScript Errors**
```javascript
// Common error patterns to look for:
TypeError: Cannot read property 'innerHTML' of null
ReferenceError: apiClient is not defined
SyntaxError: Unexpected token
CORS error: Access blocked by CORS policy
```

**2. Network Tab - API Calls**
```
✅ Status 200: Request successful
❌ Status 404: Endpoint not found
❌ Status 500: Internal server error
❌ Status 0: Connection refused (backend down)
❌ CORS: Preflight request failed
```

**3. Sources Tab - Debugging JavaScript**
```javascript
// Set breakpoints in script.js
function startProcessing() {
    debugger;  // Browser will pause here
    // Continue debugging...
}
```

### 🐛 Common Frontend Issues

#### **Issue 1: Page Not Loading**
**Symptoms**: Blank page, CSS not loading, JavaScript errors

**Debug Steps**:
```bash
# Check frontend server
curl http://localhost:3000

# Check browser console for errors
# Common fixes:
1. Ensure frontend server is running
2. Clear browser cache (Ctrl+F5)
3. Check for JavaScript syntax errors
4. Verify file paths in index.html
```

**Typical Error Messages**:
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
SyntaxError: Unexpected token '<' in JSON
TypeError: Cannot read property 'addEventListener' of null
```

#### **Issue 2: File Upload Not Working**
**Symptoms**: Drag & drop doesn't work, file selection fails, validation errors

**Debug Steps**:
```javascript
// Check in browser console
console.log('File upload triggered');
console.log('Selected file:', file);
console.log('File type:', file.type);
console.log('File size:', file.size);

// Verify event listeners
document.getElementById('csv-file').addEventListener('change', handleFileUpload);
```

**Common Causes**:
- File size exceeds 100MB limit
- File type is not .csv
- JavaScript errors preventing event handlers
- Missing or incorrectly named form elements

#### **Issue 3: Processing Stuck or Failing**
**Symptoms**: Progress bars not updating, timers frozen, error messages

**Debug Steps**:
```javascript
// Check API calls in Network tab
// Look for these request patterns:
POST /api/v1/layer1/process
GET /api/v1/health

// Check console for detailed errors
console.log('API Response:', response);
console.log('Error:', error.message);

// Test backend connectivity
await apiClient.checkHealth();
```

**Common Error Patterns**:
```javascript
// Network errors
"Failed to fetch"
"ERR_CONNECTION_REFUSED"

// API errors  
"Cannot set properties of null"
"Processing failed with status 500"
"CORS policy blocked the request"
```

#### **Issue 4: Search Not Working**
**Symptoms**: Search button disabled, no results, expandable section not showing

**Debug Steps**:
```javascript
// Check processing completion
console.log('Processing ID:', processingId);
console.log('Search enabled:', searchEnabled);

// Verify search API call
const results = await apiClient.searchChunks(processingId, query);
console.log('Search results:', results);

// Check DOM elements
document.getElementById('expandable-search-section');
document.getElementById('expandable-query-input');
```

### 🔧 Common Backend Issues

#### **Issue 1: Server Won't Start**
**Symptoms**: Import errors, port conflicts, dependency issues

**Debug Steps**:
```bash
# Check Python environment
python --version                # Should be 3.8+
which python                    # Verify virtual environment

# Test imports
python -c "import fastapi"      # Test FastAPI
python -c "import pandas"       # Test Pandas
python -c "import chromadb"     # Test ChromaDB

# Check port availability
lsof -i :8000                   # Linux/macOS
netstat -ano | findstr :8000    # Windows

# Start with debug mode
python scripts/start_server.py  # Check error output
```

**Common Error Messages**:
```python
ModuleNotFoundError: No module named 'fastapi'
ImportError: cannot import name 'xxx' from 'yyy'
OSError: [Errno 48] Address already in use
PermissionError: [Errno 13] Permission denied
```

#### **Issue 2: Processing Pipeline Failures**
**Symptoms**: API returns 500 errors, processing never completes, partial results

**Debug Steps**:
```bash
# Check application logs
grep -A 5 -B 5 "ERROR" logs/app.log

# Test individual components
python test_backend.py

# Test with minimal data
echo "name,age\nJohn,25" | base64  # Create test CSV

# Check memory usage
top -p $(pgrep -f "start_server")  # Monitor resources
```

**Log Investigation**:
```bash
# Look for these error patterns in logs:
"Pipeline failed"
"Chunking failed"
"Embedding failed"
"Storage failed"
"Memory error"
"Timeout"
```

#### **Issue 3: Vector Database Issues**
**Symptoms**: Storage fails, search returns no results, database corruption

**Debug Steps**:
```bash
# Check database directories
ls -la backend/storage/.chroma/
ls -la backend/storage/.faiss/

# Check permissions
chmod -R 755 backend/storage/

# Clear and recreate databases
rm -rf backend/storage/.chroma/*
rm -rf backend/storage/.faiss/*

# Test database connectivity
python -c "
import chromadb
client = chromadb.Client()
print('ChromaDB working')
"
```

#### **Issue 4: File Download Problems**
**Symptoms**: Download links broken, files not generated, 404 errors

**Debug Steps**:
```bash
# Check downloads directory
ls -la backend/storage/downloads/

# Check file permissions
chmod 644 backend/storage/downloads/*

# Test direct file access
curl http://localhost:8000/api/v1/download/test_file.csv

# Check file handler logs
grep "file_handler" logs/app.log
```

### 🔍 Step-by-Step Debugging Workflows

#### **Workflow 1: Complete System Check**
```bash
# 1. Environment Check
python --version
pip list | grep -E "(fastapi|pandas|chromadb)"

# 2. Backend Health
curl http://localhost:8000/api/v1/health

# 3. Frontend Access
curl -I http://localhost:3000

# 4. Test Processing
curl -X POST "http://localhost:8000/api/v1/layer1/process" \
  -H "Content-Type: application/json" \
  -d '{"csv_data": "bmFtZSxhZ2UKSm9obiwyNQ==", "filename": "test.csv"}'

# 5. Check Logs
tail -f logs/app.log
```

#### **Workflow 2: Frontend-Specific Debugging**
```javascript
// 1. Check initialization
console.log('App initialized:', window.apiClient);

// 2. Test file upload
const fileInput = document.getElementById('csv-file');
console.log('File input:', fileInput);

// 3. Test API connectivity
apiClient.checkHealth().then(console.log).catch(console.error);

// 4. Monitor processing
window.activeTimers = new Map(); // Inspect timers

// 5. Check DOM updates
const steps = document.querySelectorAll('.process-step');
console.log('Processing steps:', steps.length);
```

#### **Workflow 3: Backend Processing Debug**
```python
# Create debug script: debug_processing.py
import asyncio
from backend.services.pipeline import run_complete_pipeline
from backend.utils.helpers import get_layer_defaults

async def debug_processing():
    # Test data
    csv_data = "bmFtZSxhZ2UKSm9obiwyNQpKYW5lLDMw"
    filename = "debug_test.csv"
    config = get_layer_defaults("fast")
    
    try:
        result = await run_complete_pipeline(csv_data, filename, config)
        print("✅ Processing successful:", result['success'])
        print("📊 Summary:", result['processing_summary'])
    except Exception as e:
        print("❌ Processing failed:", e)
        import traceback
        traceback.print_exc()

# Run debug
asyncio.run(debug_processing())
```

### 🚨 Emergency Troubleshooting

#### **Quick Reset Commands**
```bash
# Nuclear option - reset everything
pkill -f "python scripts"       # Kill all processes
rm -rf backend/storage/.chroma/* # Clear ChromaDB
rm -rf backend/storage/.faiss/*  # Clear FAISS
rm -rf backend/storage/downloads/* # Clear downloads
rm -rf backend/storage/temp_files/* # Clear temp files

# Restart cleanly
python scripts/start_full_stack.py
```

#### **Environment Repair**
```bash
# Recreate virtual environment
deactivate                      # Exit current environment
rm -rf chunker_env              # Remove old environment
python -m venv chunker_env      # Create new environment
source chunker_env/bin/activate # Activate (Linux/macOS)
pip install -r requirements.txt # Reinstall dependencies
python -m spacy download en_core_web_sm # Download models
```

#### **Database Repair**
```bash
# ChromaDB repair
python -c "
import chromadb
import shutil
import os

# Clear corrupted database
if os.path.exists('backend/storage/.chroma'):
    shutil.rmtree('backend/storage/.chroma')

# Create fresh database
client = chromadb.PersistentClient(path='backend/storage/.chroma')
print('ChromaDB repaired')
"
```

### 📊 Performance Debugging

#### **Memory Issues**
```bash
# Monitor memory usage
python -c "
import psutil
import os

# Get current process
process = psutil.Process()
print(f'Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB')
print(f'CPU: {process.cpu_percent()}%')

# Monitor during processing
"

# Check system memory
free -h                         # Linux
vm_stat                         # macOS
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory # Windows
```

#### **Network Issues**
```bash
# Test network connectivity
ping localhost                  # Basic connectivity
telnet localhost 8000          # Test specific port
curl -v http://localhost:8000/api/v1/health # Verbose HTTP test

# Check firewall
sudo ufw status                 # Linux
netsh advfirewall show allprofiles # Windows
```

#### **File System Issues**
```bash
# Check disk space
df -h                          # Linux/macOS
dir C:\                        # Windows

# Check permissions
ls -la backend/storage/        # View permissions
whoami                         # Current user
```

### 🔧 Developer Tools & Scripts

#### **Custom Debug Script**
Create `debug_app.py`:
```python
#!/usr/bin/env python3
"""
CSV Chunker Pro Debug Utility
"""

import asyncio
import requests
import json
import base64
from pathlib import Path

class DebugApp:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        
    def test_health(self):
        """Test backend health"""
        try:
            response = requests.get(f"{self.base_url}/api/v1/health")
            print(f"✅ Health: {response.status_code}")
            return response.json()
        except Exception as e:
            print(f"❌ Health failed: {e}")
            return None
    
    def test_processing(self):
        """Test minimal processing"""
        csv_data = base64.b64encode(b"name,age\nJohn,25").decode()
        
        try:
            response = requests.post(f"{self.base_url}/api/v1/layer1/process", 
                json={"csv_data": csv_data, "filename": "test.csv"})
            print(f"✅ Processing: {response.status_code}")
            return response.json()
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            return None
    
    def run_all_tests(self):
        """Run complete debug suite"""
        print("🔍 CSV Chunker Pro Debug Suite")
        print("=" * 40)
        
        health = self.test_health()
        processing = self.test_processing()
        
        print("\n📊 Summary:")
        print(f"Health: {'✅' if health else '❌'}")
        print(f"Processing: {'✅' if processing else '❌'}")

if __name__ == "__main__":
    debug = DebugApp()
    debug.run_all_tests()
```

#### **Log Analysis Script**
Create `analyze_logs.py`:
```python
#!/usr/bin/env python3
"""
Log Analysis Utility
"""

import re
from collections import Counter
from pathlib import Path

def analyze_logs(log_file="logs/app.log"):
    """Analyze application logs for patterns"""
    
    if not Path(log_file).exists():
        print(f"❌ Log file not found: {log_file}")
        return
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    # Count error levels
    levels = Counter()
    errors = []
    
    for line in lines:
        if "ERROR" in line:
            levels["ERROR"] += 1
            errors.append(line.strip())
        elif "WARNING" in line:
            levels["WARNING"] += 1
        elif "INFO" in line:
            levels["INFO"] += 1
    
    print("📊 Log Analysis Results")
    print("=" * 30)
    print(f"Total lines: {len(lines)}")
    print(f"Error levels: {dict(levels)}")
    
    if errors:
        print(f"\n❌ Recent errors ({len(errors)} total):")
        for error in errors[-5:]:  # Last 5 errors
            print(f"  {error}")

if __name__ == "__main__":
    analyze_logs()
```

### 📝 Debug Checklist

When reporting issues, include this information:

#### **Environment Info**
- [ ] Operating System and version
- [ ] Python version (`python --version`)
- [ ] Virtual environment status
- [ ] Installed packages (`pip list`)
- [ ] Browser and version (for frontend issues)

#### **Error Details**
- [ ] Exact error message
- [ ] Steps to reproduce
- [ ] Expected vs actual behavior
- [ ] Screenshots (for UI issues)
- [ ] Relevant log entries

#### **System State**
- [ ] Backend server status
- [ ] Frontend server status
- [ ] File system permissions
- [ ] Available disk space and memory
- [ ] Network connectivity

#### **Attempted Solutions**
- [ ] Restart servers
- [ ] Clear cache/cookies
- [ ] Check logs
- [ ] Test with minimal data
- [ ] Environment recreation

This debugging guide provides systematic approaches to identify and resolve issues across all components of CSV Chunker Pro.

---

## 8. Error Handling Matrix

### 📊 Complete Error Reference Table

| **Error Type** | **Possible Cause** | **File to Check** | **Solution** |
|----------------|---------------------|-------------------|--------------|
| **Frontend JavaScript Errors** |
| `Cannot read property 'innerHTML' of null` | DOM element not found | `frontend/script.js` | Add null checks before DOM manipulation |
| `ReferenceError: apiClient is not defined` | API client not initialized | `frontend/script.js` | Ensure `apiClient = new APIClient()` runs |
| `TypeError: Cannot read property 'addEventListener' of null` | Element doesn't exist when script runs | `frontend/index.html` | Move scripts to end of body or use DOMContentLoaded |
| `SyntaxError: Unexpected token '<' in JSON` | API returning HTML instead of JSON | Network tab, backend logs | Check API endpoint URL and server response |
| `Failed to fetch` | Network connectivity issue | Browser console | Verify backend is running, check CORS settings |
| **File Upload Errors** |
| `File size exceeds maximum limit` | File larger than 100MB | `frontend/script.js` | Use smaller file or increase `MAX_FILE_SIZE_MB` |
| `Invalid file type` | Non-CSV file uploaded | `frontend/script.js` | Ensure file has .csv extension |
| `Cannot read property 'files' of null` | File input element missing | `frontend/index.html` | Check file input ID matches JavaScript |
| `FileReader not supported` | Old browser | Browser console | Use modern browser (Chrome 5+, Firefox 3.6+) |
| **API/Network Errors** |
| `CORS policy blocked request` | Cross-origin restriction | `config/settings.py` | Add frontend URL to `CORS_ORIGINS` |
| `ERR_CONNECTION_REFUSED` | Backend server not running | Terminal | Start backend with `python scripts/start_server.py` |
| `404 Not Found` | Wrong API endpoint | Network tab | Verify endpoint URL in `frontend/script.js` |
| `500 Internal Server Error` | Backend processing failure | `logs/app.log` | Check backend logs for specific error |
| `Timeout` | Request taking too long | Browser console | Increase timeout or use smaller file |
| **Backend Startup Errors** |
| `ModuleNotFoundError: No module named 'fastapi'` | Missing dependencies | Terminal | Run `pip install -r requirements.txt` |
| `ImportError: cannot import name 'settings'` | Configuration issue | `config/settings.py` | Verify settings file exists and syntax |
| `OSError: [Errno 48] Address already in use` | Port 8000 occupied | Terminal | Kill process or change port in settings |
| `PermissionError: [Errno 13] Permission denied` | Insufficient permissions | File system | Fix directory permissions with `chmod` |
| `FileNotFoundError: [Errno 2] No such file` | Missing required files | Project structure | Ensure all files from repository are present |
| **Processing Pipeline Errors** |
| `Pipeline failed: Chunking error` | Chunking algorithm failure | `backend/core/chunking.py` | Check data format, try different chunking method |
| `Embedding model not found` | Sentence transformer issue | Terminal | Run `pip install sentence-transformers` |
| `ChromaDB connection failed` | Vector database issue | `backend/storage/.chroma/` | Clear database or check permissions |
| `Memory error` | Insufficient RAM | System monitor | Use smaller file or increase system memory |
| `JSON decode error` | Corrupted data | `logs/app.log` | Verify CSV data format and encoding |
| **Database Errors** |
| `ChromaDB: Collection not found` | Database initialization issue | `backend/storage/.chroma/` | Delete and recreate database |
| `FAISS: Index file corrupted` | Vector index corruption | `backend/storage/.faiss/` | Clear FAISS directory and reprocess |
| `Disk space error` | Storage full | File system | Free up disk space or change storage location |
| `Database lock error` | Concurrent access issue | Application logs | Restart application to release locks |
| **File Download Errors** |
| `Download link expired` | File retention timeout | `backend/storage/downloads/` | Reprocess data to generate new files |
| `404: File not found` | Download file missing | Download directory | Check if processing completed successfully |
| `Permission denied on download` | File access rights | File permissions | Set correct permissions with `chmod 644` |
| `Corrupted ZIP file` | Archive creation failed | Backend logs | Check available disk space and retry |
| **Search/Retrieval Errors** |
| `No results found` | Empty vector database | Database files | Verify data was processed and stored |
| `Query embedding failed` | Model loading issue | Backend logs | Check sentence-transformers installation |
| `Similarity search timeout` | Large dataset performance | Performance monitor | Use smaller top_k value or optimize index |
| `Invalid query format` | Special characters in query | Frontend validation | Sanitize query input |
| **Performance Issues** |
| `Processing extremely slow` | Large file or insufficient resources | System monitor | Use smaller batches or upgrade hardware |
| `High memory usage` | Memory leaks | Process monitor | Restart application or optimize batch size |
| `CPU at 100%` | Intensive processing | Task manager | Normal during embedding generation |
| `Disk I/O errors` | Storage device issues | System logs | Check disk health and free space |
| **Configuration Errors** |
| `Settings not loading` | Environment variables wrong | `.env` file | Verify environment variable format |
| `Layer defaults missing` | Configuration corruption | `config/settings.py` | Restore default settings from repository |
| `Invalid chunking parameters` | Wrong configuration values | Layer configuration | Use valid parameters (positive integers) |
| `Model download failed` | Network or storage issue | Terminal | Manually download model or check internet |
| **UI/Display Errors** |
| `Progress bars not updating` | JavaScript timer issues | Browser console | Refresh page or check for errors |
| `Download buttons not appearing` | DOM insertion failure | Frontend logs | Check processing completion status |
| `Search section not expanding` | Event listener missing | Frontend debugging | Verify click handlers are attached |
| `Misaligned elements` | CSS conflicts | Browser dev tools | Check CSS styles and responsive design |
| **Security Errors** |
| `HTTPS required` | SSL certificate issue | Server configuration | Configure SSL or use HTTP for development |
| `Content Security Policy violation` | Browser security restriction | Browser console | Adjust CSP headers or use allowed sources |
| `File upload blocked` | Antivirus software | System security | Whitelist application or disable scanning |

### 🚨 Critical Error Scenarios

#### **Scenario 1: Complete System Failure**
```
Symptoms: Nothing works, servers won't start, multiple errors
Diagnosis: Environment corruption or major dependency issue
Solution: Nuclear reset - recreate environment from scratch
```

**Recovery Steps**:
```bash
# 1. Complete cleanup
pkill -f python                     # Kill all Python processes
rm -rf chunker_env                  # Remove virtual environment
rm -rf backend/storage/.chroma/*    # Clear databases
rm -rf backend/storage/.faiss/*     # Clear indexes
rm -rf __pycache__                  # Clear Python cache

# 2. Fresh installation
python -m venv chunker_env          # New environment
source chunker_env/bin/activate     # Activate
pip install --upgrade pip           # Latest pip
pip install -r requirements.txt     # Dependencies
python -m spacy download en_core_web_sm # Models

# 3. Test installation
python test_backend.py              # Verify backend
python scripts/start_full_stack.py  # Start application
```

#### **Scenario 2: Data Corruption**
```
Symptoms: Processing succeeds but results are wrong
Diagnosis: Vector database or file corruption
Solution: Clear storage and reprocess
```

**Recovery Steps**:
```bash
# Clear all generated data
rm -rf backend/storage/downloads/*
rm -rf backend/storage/temp_files/*
rm -rf backend/storage/.chroma/*
rm -rf backend/storage/.faiss/*

# Restart and reprocess
python scripts/start_full_stack.py
# Upload file again through UI
```

#### **Scenario 3: Performance Degradation**
```
Symptoms: System becomes progressively slower
Diagnosis: Memory leaks or resource exhaustion  
Solution: Restart and optimize settings
```

**Recovery Steps**:
```bash
# Monitor resources
top | grep python                   # Check CPU/memory
df -h                               # Check disk space

# Restart application
pkill -f "start_server"
python scripts/start_full_stack.py

# Optimize settings in config/settings.py:
MAX_FILE_SIZE_MB = 50              # Reduce max file size
DEFAULT_BATCH_SIZE = 16            # Smaller batches
```

### 🔧 Error Prevention Strategies

#### **1. Proactive Monitoring**
```bash
# Regular health checks
curl http://localhost:8000/api/v1/health

# Log monitoring
tail -f logs/app.log | grep -E "(ERROR|WARNING)"

# Resource monitoring  
free -h && df -h
```

#### **2. Environment Validation**
```python
# Create environment_check.py
import sys
import subprocess
import pkg_resources

def check_environment():
    # Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Required packages
    required = ['fastapi', 'pandas', 'chromadb', 'sentence-transformers']
    for package in required:
        try:
            pkg_resources.get_distribution(package)
            print(f"✅ {package}")
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package} missing")
            return False
    
    return True

if __name__ == "__main__":
    check_environment()
```

#### **3. Input Validation**
```javascript
// Enhanced file validation
function validateCSVFile(file) {
    // Check file type
    if (!file.name.toLowerCase().endsWith('.csv')) {
        throw new Error('File must be a CSV file');
    }
    
    // Check file size (100MB limit)
    if (file.size > 100 * 1024 * 1024) {
        throw new Error('File size must be less than 100MB');
    }
    
    // Check if file is empty
    if (file.size === 0) {
        throw new Error('File cannot be empty');
    }
    
    return true;
}
```

#### **4. Error Boundary Implementation**
```javascript
// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    
    // Show user-friendly message
    showErrorMessage('An unexpected error occurred. Please refresh the page.');
    
    // Log to backend (if available)
    if (window.apiClient) {
        apiClient.logError(e.error.message, e.error.stack);
    }
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    showErrorMessage('A network or processing error occurred.');
});
```

### 📱 Quick Error Resolution Commands

#### **Most Common Issues - One-Line Fixes**
```bash
# Backend not responding
pkill python && python scripts/start_server.py

# Frontend not loading  
pkill -f "start_frontend" && python scripts/start_frontend.py

# CORS errors
echo 'CORS_ORIGINS = ["*"]' >> config/settings.py

# Database issues
rm -rf backend/storage/.chroma/* && rm -rf backend/storage/.faiss/*

# Permission errors
chmod -R 755 backend/storage/

# Memory issues
echo 'DEFAULT_BATCH_SIZE = 16' >> config/settings.py

# Module not found
pip install -r requirements.txt

# Port conflicts
export PORT=8001 && python scripts/start_server.py
```

#### **Emergency Diagnostic Commands**
```bash
# Quick system check
python --version && pip list | grep fastapi && curl -I localhost:8000/api/v1/health

# Complete error scan
grep -r "ERROR\|FAILED\|Exception" logs/ 2>/dev/null | tail -10

# Resource check
free -h && df -h && ps aux | grep python

# Network check
netstat -tlnp | grep -E "(3000|8000)" 2>/dev/null || ss -tlnp | grep -E "(3000|8000)"
```

This error matrix provides a comprehensive reference for troubleshooting any issue that may arise in CSV Chunker Pro, organized by error type with specific solutions for each scenario.

---

## 9. API Documentation

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

## 10. Database Schema

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

## 11. Frontend Components

### 🎨 UI Architecture Overview

The CSV Chunker Pro frontend is built as a single-page application using vanilla HTML, CSS, and JavaScript with a component-based approach:

```
App Container
├── Sidebar (Processing Pipeline + Stats)
└── Main Content
    ├── Layer Selection
    ├── File Upload Area  
    ├── Configuration Sections
    ├── Action Buttons
    ├── Download Section (Dynamic)
    └── Search Section (Dynamic)
```

### 🏗️ HTML Structure Breakdown

#### **Root Container**
```html
<div class="app-container">
    <!-- Main application wrapper -->
</div>
```

**Purpose**: Top-level container with flexbox layout
**CSS Classes**: `.app-container`
**Responsive**: Switches to column layout on mobile

#### **Sidebar Component**
```html
<div class="sidebar">
    <div class="sidebar-header">
        <h1>CSV Chunking Optimizer Pro</h1>
    </div>
    
    <div class="processing-pipeline">
        <!-- 6 processing steps -->
    </div>
    
    <div class="stats-section">
        <!-- Processing statistics -->
    </div>
</div>
```

**Key Elements**:
- **Header**: Application title and branding
- **Pipeline**: 6-step processing visualization
- **Stats**: Real-time processing metrics

**JavaScript Interactions**:
- Progress step updates
- Timer management
- Status text changes

#### **Main Content Area**
```html
<div class="main-content">
    <div class="content-section active" id="layer-1-content">
        <!-- Layer 1 content -->
    </div>
    <div class="content-section" id="layer-2-content">
        <!-- Layer 2 content -->
    </div>
    <div class="content-section" id="layer-3-content">
        <!-- Layer 3 content -->
    </div>
</div>
```

**Dynamic Sections**:
- Layer-specific content switching
- Configuration panels
- Generated download/search sections

### 📱 Component Detailed Breakdown

#### **1. Layer Selection Component**
```html
<div class="layer-selector">
    <input type="radio" id="layer-1" name="layer" value="1" checked>
    <label for="layer-1" class="layer-option">
        <div class="layer-icon">⚡</div>
        <div class="layer-content">
            <div class="layer-title">Layer 1 - Fast</div>
            <div class="layer-description">Quick processing with optimized defaults</div>
        </div>
    </label>
    <!-- More layer options... -->
</div>
```

**JavaScript Handler**:
```javascript
function selectLayer(layerNumber) {
    currentLayer = layerNumber;
    
    // Update UI
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(`layer-${layerNumber}-content`).classList.add('active');
    
    // Update radio button
    document.getElementById(`layer-${layerNumber}`).checked = true;
    
    console.log(`Layer ${layerNumber} selected`);
}
```

**Features**:
- Radio button selection
- Visual feedback with icons
- Content switching animation
- Keyboard navigation support

#### **2. File Upload Component**
```html
<div class="upload-section">
    <div class="upload-area" id="upload-area">
        <div class="upload-icon">📁</div>
        <div class="upload-text">
            <div class="upload-title">Upload CSV File</div>
            <div class="upload-subtitle">Drag & drop or click to select</div>
        </div>
        <input type="file" id="csv-file" accept=".csv" hidden>
    </div>
    <div class="file-info" id="file-info" style="display: none;">
        <!-- File details display -->
    </div>
</div>
```

**JavaScript Handlers**:
```javascript
// File selection handler
function handleFileUpload(event) {
    const file = event.target.files[0] || event.dataTransfer.files[0];
    
    if (!validateCSVFile(file)) {
        showError("Invalid file type or size");
        return;
    }
    
    displayFileInfo(file);
    currentFile = file;
}

// Drag and drop handlers
function handleDragOver(event) {
    event.preventDefault();
    document.getElementById('upload-area').classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    document.getElementById('upload-area').classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    document.getElementById('upload-area').classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload({ target: { files } });
    }
}
```

**Features**:
- Drag & drop support
- File validation (type, size)
- Visual feedback during drag
- File information display
- Error handling

#### **3. Processing Pipeline Component**
```html
<div class="processing-pipeline">
    <div class="process-step" id="step-upload">
        <div class="step-content">
            <div class="step-details">
                <div class="step-title">File Upload</div>
                <div class="step-description">CSV file selection</div>
            </div>
            <div class="step-right-container">
                <span class="step-status-text"></span>
                <span class="step-timing"></span>
                <div class="step-status">📁</div>
            </div>
        </div>
    </div>
    <!-- 5 more steps... -->
</div>
```

**JavaScript Management**:
```javascript
// Step state management
function updateStepStatus(stepId, status) {
    const step = document.getElementById(stepId);
    
    // Remove all status classes
    step.classList.remove('pending', 'active', 'completed', 'error');
    
    // Add new status
    step.classList.add(status);
    
    // Update icon based on status
    const statusElement = step.querySelector('.step-status');
    switch(status) {
        case 'active':
            statusElement.innerHTML = '🔄';
            break;
        case 'completed':
            statusElement.innerHTML = '✅';
            break;
        case 'error':
            statusElement.innerHTML = '❌';
            break;
    }
}

// Timer functions for live updates
function startStepTimer(stepId, stepName) {
    const startTime = Date.now();
    
    updateStepStatus(stepId, 'active');
    updateStepStatusText(stepId, 'Processing');
    
    const intervalId = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        updateStepLiveTime(stepId, elapsed);
    }, 1000);
    
    activeTimers.set(stepId, { startTime, intervalId, stepName });
}
```

**Features**:
- Real-time status updates
- Live timing display
- Visual progress indicators
- Status text management
- Responsive layout

#### **4. Configuration Panels**
```html
<div class="config-section">
    <div class="config-card">
        <div class="config-card-header">
            <div class="config-icon">🔧</div>
            <div class="config-title">Preprocessing</div>
        </div>
        <div class="config-card-content">
            <div class="config-row">
                <label class="config-label">Remove Duplicates</label>
                <div class="toggle-switch">
                    <input type="checkbox" id="remove-duplicates" checked>
                    <label for="remove-duplicates" class="toggle-slider"></label>
                </div>
            </div>
            <!-- More config options... -->
        </div>
    </div>
</div>
```

**JavaScript Configuration**:
```javascript
function getLayerConfiguration(layerNumber) {
    const config = {};
    
    // Collect all form inputs for the layer
    const layerContent = document.getElementById(`layer-${layerNumber}-content`);
    const inputs = layerContent.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        if (input.type === 'checkbox') {
            config[input.id] = input.checked;
        } else if (input.type === 'number') {
            config[input.id] = parseInt(input.value);
        } else {
            config[input.id] = input.value;
        }
    });
    
    return config;
}
```

**Features**:
- Toggle switches
- Number inputs with validation
- Dropdown selections
- Dynamic configuration loading
- Form state persistence

#### **5. Action Buttons Component**
```html
<div class="action-buttons">
    <button class="btn btn-secondary" onclick="resetConfiguration()">
        <span class="btn-icon">🔄</span>
        <span class="btn-text">Reset</span>
    </button>
    
    <button class="btn btn-secondary" onclick="saveConfiguration()">
        <span class="btn-icon">💾</span>
        <span class="btn-text">Save Config</span>
    </button>
    
    <button class="btn btn-primary" id="start-processing" onclick="startProcessing()">
        <span class="btn-icon">🚀</span>
        <span class="btn-text">Start Processing</span>
    </button>
</div>
```

**JavaScript Actions**:
```javascript
function resetConfiguration() {
    // Reset all form inputs to defaults
    document.querySelectorAll('input, select').forEach(input => {
        if (input.type === 'checkbox') {
            input.checked = input.hasAttribute('checked');
        } else {
            input.value = input.defaultValue;
        }
    });
    
    showSuccess('Configuration reset to defaults');
}

function saveConfiguration() {
    const config = getLayerConfiguration(currentLayer);
    localStorage.setItem('csvChunkerConfig', JSON.stringify(config));
    showSuccess('Configuration saved');
}

async function startProcessing() {
    if (!currentFile) {
        showError('Please select a CSV file first');
        return;
    }
    
    // Disable button during processing
    const button = document.getElementById('start-processing');
    button.disabled = true;
    button.innerHTML = '<span class="btn-icon">⏳</span><span class="btn-text">Processing...</span>';
    
    try {
        await processDynamicStepByStep(currentFile);
    } catch (error) {
        handleProcessingError(error);
    } finally {
        // Re-enable button
        button.disabled = false;
        button.innerHTML = '<span class="btn-icon">🚀</span><span class="btn-text">Start Processing</span>';
    }
}
```

**Features**:
- Button state management
- Loading indicators
- Configuration persistence
- Error handling
- Accessibility support

#### **6. Dynamic Download Section**
```javascript
function showRealDownloadButtons(downloadLinks) {
    let downloadSection = document.getElementById('download-section');
    
    if (!downloadSection) {
        downloadSection = document.createElement('div');
        downloadSection.id = 'download-section';
        downloadSection.className = 'config-card';
        
        // Dynamic positioning and styling
        downloadSection.style.cssText = `
            margin: -150px auto 15px auto;
            max-width: 800px;
            width: 100%;
            background: #1d2224;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 12px;
            position: relative;
            z-index: 999;
            height: auto;
            min-height: 100px;
            overflow: visible;
            top: -60px;
        `;
    }
    
    // Create download buttons
    const buttonsHTML = Object.entries(downloadLinks).map(([type, info]) => `
        <button class="btn btn-download" onclick="downloadFile('${info.url}', '${info.filename}')">
            <span class="btn-icon">${getFileIcon(type)}</span>
            <span class="btn-text">${info.filename}</span>
            <span class="file-size">${formatFileSize(info.size_bytes)}</span>
        </button>
    `).join('');
    
    downloadSection.innerHTML = `
        <div class="config-card-header">
            <div class="config-icon">📁</div>
            <div class="config-title">Download Processed Files</div>
        </div>
        <div class="download-buttons" id="download-buttons">
            ${buttonsHTML}
        </div>
    `;
    
    // Insert into DOM at optimal position
    insertDownloadSection(downloadSection);
}
```

**Features**:
- Dynamic creation and positioning
- File type icons
- Size formatting
- Download functionality
- Responsive layout

#### **7. Expandable Search Section**
```javascript
function enableExpandableSearchInterface(processingId) {
    let searchSection = document.getElementById('expandable-search-section');
    
    if (!searchSection) {
        searchSection = document.createElement('div');
        searchSection.id = 'expandable-search-section';
        
        searchSection.innerHTML = `
            <!-- Collapsed Header -->
            <div id="search-header" class="expandable-header" onclick="toggleSearchSection()">
                <div class="header-content">
                    <div class="header-icon">🔍</div>
                    <div class="header-title">Search Retrieved Chunks</div>
                    <div class="header-subtitle">Click to expand search interface</div>
                </div>
                <div class="toggle-icon" id="search-toggle-icon">▼</div>
            </div>
            
            <!-- Expandable Content -->
            <div id="search-content" class="expandable-content" style="display: none;">
                <div class="search-controls">
                    <input type="text" id="expandable-query-input" placeholder="Enter your search query...">
                    <select id="expandable-similarity-metric">
                        <option value="cosine">Cosine</option>
                        <option value="dot">Dot Product</option>
                        <option value="euclidean">Euclidean</option>
                    </select>
                    <input type="number" id="expandable-top-k" value="5" min="1" max="20">
                    <button onclick="performExpandableSearch('${processingId}')">Search</button>
                </div>
                <div id="expandable-search-results" class="search-results"></div>
            </div>
        `;
    }
    
    // Insert after download section
    insertSearchSection(searchSection);
}

function toggleSearchSection() {
    const content = document.getElementById('search-content');
    const toggleIcon = document.getElementById('search-toggle-icon');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        toggleIcon.textContent = '▲';
    } else {
        content.style.display = 'none';
        toggleIcon.textContent = '▼';
    }
}
```

**Features**:
- Collapsible interface
- Search controls
- Results display
- Keyboard shortcuts
- Smooth animations

### 🎛️ Event Handling System

#### **Global Event Listeners**
```javascript
function initializeApp() {
    // File upload events
    document.getElementById('csv-file').addEventListener('change', handleFileUpload);
    document.getElementById('upload-area').addEventListener('click', () => {
        document.getElementById('csv-file').click();
    });
    
    // Drag and drop events
    const uploadArea = document.getElementById('upload-area');
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Layer selection events
    document.querySelectorAll('input[name="layer"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            selectLayer(parseInt(e.target.value));
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
    
    // Window events
    window.addEventListener('beforeunload', handleBeforeUnload);
    window.addEventListener('error', handleGlobalError);
    
    console.log('CSV Chunking Optimizer initialized successfully!');
}
```

#### **Keyboard Shortcuts**
```javascript
function handleKeyboardShortcuts(event) {
    // Ctrl/Cmd + Enter: Start processing
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        if (currentFile) {
            startProcessing();
        }
    }
    
    // Ctrl/Cmd + R: Reset configuration
    if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
        event.preventDefault();
        resetConfiguration();
    }
    
    // Escape: Close modals or cancel operations
    if (event.key === 'Escape') {
        closeModals();
    }
    
    // Enter in search box: Perform search
    if (event.key === 'Enter' && event.target.id === 'expandable-query-input') {
        const processingId = getCurrentProcessingId();
        if (processingId) {
            performExpandableSearch(processingId);
        }
    }
}
```

### 🎨 CSS Component Styling

#### **Responsive Breakpoints**
```css
/* Mobile First Approach */
@media (max-width: 768px) {
    .app-container {
        flex-direction: column;
    }
    
    .sidebar {
        width: 100%;
        height: auto;
    }
    
    .main-content {
        padding: 15px;
    }
    
    .layer-selector {
        flex-direction: column;
    }
}

@media (max-width: 480px) {
    .config-row {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .action-buttons {
        flex-direction: column;
        gap: 10px;
    }
    
    .btn {
        width: 100%;
    }
}
```

#### **Animation System**
```css
/* Smooth transitions */
.process-step {
    transition: all 0.3s ease;
}

.process-step.active {
    background: rgba(74, 144, 226, 0.1);
    border-left: 3px solid #4a90e2;
}

.upload-area {
    transition: all 0.2s ease;
}

.upload-area:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(74, 144, 226, 0.2);
}

.upload-area.dragover {
    background: rgba(74, 144, 226, 0.1);
    border-color: #4a90e2;
    transform: scale(1.02);
}

/* Button animations */
.btn {
    transition: all 0.2s ease;
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
```

### 🔧 State Management

#### **Global State Variables**
```javascript
// Application state
let currentLayer = 1;
let currentFile = null;
let currentProcessingId = null;
let apiClient = null;

// UI state
const activeTimers = new Map();
let isProcessing = false;
let searchEnabled = false;

// Configuration state
let layerConfigurations = {
    1: {},  // Layer 1 config
    2: {},  // Layer 2 config
    3: {}   // Layer 3 config
};
```

#### **State Update Functions**
```javascript
function updateApplicationState(newState) {
    Object.assign(window.appState, newState);
    
    // Trigger UI updates based on state changes
    if (newState.hasOwnProperty('isProcessing')) {
        updateProcessingUI(newState.isProcessing);
    }
    
    if (newState.hasOwnProperty('currentFile')) {
        updateFileDisplay(newState.currentFile);
    }
}

function getApplicationState() {
    return {
        currentLayer,
        currentFile: currentFile ? currentFile.name : null,
        currentProcessingId,
        isProcessing,
        searchEnabled,
        activeTimersCount: activeTimers.size
    };
}
```

### 📱 Mobile Responsiveness

#### **Touch Events**
```javascript
// Touch support for mobile devices
function addTouchSupport() {
    // Touch-friendly file upload
    const uploadArea = document.getElementById('upload-area');
    uploadArea.addEventListener('touchstart', handleTouchStart, { passive: true });
    
    // Swipe gestures for layer switching
    let touchStartX = 0;
    let touchEndX = 0;
    
    document.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    
    document.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipeGesture();
    }, { passive: true });
    
    function handleSwipeGesture() {
        const swipeThreshold = 100;
        const diff = touchStartX - touchEndX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                // Swipe left - next layer
                if (currentLayer < 3) selectLayer(currentLayer + 1);
            } else {
                // Swipe right - previous layer
                if (currentLayer > 1) selectLayer(currentLayer - 1);
            }
        }
    }
}
```

#### **Mobile-Optimized Components**
```css
/* Mobile-specific styles */
@media (max-width: 768px) {
    .upload-area {
        min-height: 120px;
        padding: 20px;
    }
    
    .processing-pipeline {
        padding: 10px;
    }
    
    .process-step {
        padding: 12px;
        margin: 6px 0;
    }
    
    .btn {
        min-height: 44px;  /* iOS touch target size */
        padding: 12px 20px;
    }
    
    .config-card {
        margin: 10px 0;
        padding: 15px;
    }
}
```

This comprehensive frontend documentation covers all UI components, their interactions, styling, and responsive behavior in the CSV Chunker Pro application.

---

## 12. Configuration Files

### 📄 Configuration Overview

CSV Chunker Pro uses several configuration files to manage dependencies, settings, and application behavior. Understanding these files is crucial for customization, deployment, and troubleshooting.

### 📦 Python Dependencies - `requirements.txt`

#### **File Purpose**
Defines all Python packages required to run the application, with version constraints for stability and compatibility.

#### **Dependency Categories**

##### **Core Data Processing**
```python
pandas>=2.0.0          # Data manipulation and analysis
numpy>=1.24.0          # Numerical computing and array operations
scikit-learn>=1.3.0    # Machine learning utilities (KMeans clustering)
```

**Purpose**: These packages handle CSV data loading, preprocessing, and clustering algorithms.

**Version Requirements**:
- **pandas 2.0+**: Required for modern DataFrame operations and performance improvements
- **numpy 1.24+**: Needed for advanced array operations and memory efficiency
- **scikit-learn 1.3+**: Required for semantic chunking with KMeans clustering

##### **Text Processing & NLP**
```python
nltk>=3.8                    # Natural language processing toolkit
spacy>=3.6.0                 # Advanced NLP library for text processing
sentence-transformers>=2.2.2 # Generate semantic embeddings
langchain>=0.1.0             # Text splitting and chunking utilities
langchain-text-splitters>=0.0.1 # Specialized text splitting tools
tiktoken>=0.5.0              # Token counting for text processing
```

**Purpose**: Handle text preprocessing, tokenization, and semantic embedding generation.

**Critical Dependencies**:
- **sentence-transformers**: Core component for generating vector embeddings
- **langchain**: Provides advanced text chunking algorithms
- **tiktoken**: Accurate token counting for chunk size management

##### **Vector Databases**
```python
chromadb>=0.4.0        # Easy-to-use vector database for development
faiss-cpu>=1.7.4       # High-performance similarity search and clustering
```

**Purpose**: Store and retrieve vector embeddings for semantic search.

**Database Selection**:
- **ChromaDB**: Default choice for development and small datasets
- **FAISS**: Production choice for large datasets and high performance

##### **Web Scraping & Text Cleaning**
```python
beautifulsoup4>=4.12.0 # HTML/XML parsing for text cleaning
lxml>=4.9.0            # XML/HTML parser backend
chardet>=5.0.0         # Character encoding detection
```

**Purpose**: Clean and process text data from various sources.

##### **FastAPI & Web Framework**
```python
fastapi>=0.104.0       # Modern, fast web framework for building APIs
uvicorn>=0.24.0        # ASGI server for running FastAPI applications
python-multipart>=0.0.6 # Handle multipart form data and file uploads
pydantic>=2.4.0        # Data validation and serialization using Python type hints
```

**Purpose**: Provide the web API framework and server infrastructure.

**Version Requirements**:
- **FastAPI 0.104+**: Required for latest async features and security updates
- **Pydantic 2.4+**: Modern data validation with improved performance

##### **Utilities**
```python
tqdm>=4.66.0           # Progress bars for long-running operations
requests>=2.31.0       # HTTP library for API calls
python-dateutil>=2.8.0 # Date parsing and manipulation
regex>=2023.0.0        # Advanced regular expressions
typing-extensions>=4.8.0 # Extended type hints for Python
```

**Purpose**: Provide utility functions and enhanced language features.

##### **Data Validation & Serialization**
```python
jsonschema>=4.19.0     # JSON schema validation
python-json-logger>=2.0.0 # Structured logging in JSON format
```

**Purpose**: Ensure data integrity and provide structured logging.

##### **File Handling**
```python
python-magic>=0.4.27   # File type detection
aiofiles>=23.2.0       # Asynchronous file operations
```

**Purpose**: Handle file operations efficiently and securely.

##### **Development & Testing (Optional)**
```python
pytest>=7.4.0         # Testing framework
pytest-asyncio>=0.21.0 # Async testing support
black>=23.0.0          # Code formatting
isort>=5.12.0          # Import sorting
```

**Purpose**: Development tools for testing and code quality.

#### **Dependency Management Best Practices**

##### **Version Pinning Strategy**
```python
# Recommended approach: Minimum version with compatibility
pandas>=2.0.0,<3.0.0    # Allow minor updates, block major changes

# For critical dependencies: Exact pinning
fastapi==0.104.1         # Exact version for production stability

# For utilities: Loose pinning
requests>=2.31.0         # Allow updates for security patches
```

##### **Installation Commands**
```bash
# Standard installation
pip install -r requirements.txt

# Development installation with optional packages
pip install -r requirements.txt pytest black isort

# Production installation (minimal)
pip install --no-dev -r requirements.txt

# Upgrade all packages
pip install --upgrade -r requirements.txt
```

##### **Dependency Conflicts Resolution**
```bash
# Check for conflicts
pip check

# Show dependency tree
pip-tree

# Create lock file for exact reproducibility
pip freeze > requirements.lock

# Install from lock file
pip install -r requirements.lock
```

### ⚙️ Application Settings - `config/settings.py`

#### **File Structure Overview**
```python
class Settings:
    """Application settings with environment variable support"""
    
    # API Configuration
    APP_NAME: str = "CSV Chunking Optimizer Pro API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Complete CSV processing, chunking, embedding, and retrieval API"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
```

#### **Configuration Categories**

##### **API Configuration**
```python
APP_NAME: str = "CSV Chunking Optimizer Pro API"
VERSION: str = "1.0.0"
DESCRIPTION: str = "Complete CSV processing, chunking, embedding, and retrieval API"
```

**Purpose**: Define application metadata for API documentation and responses.

**Customization**:
- Change `APP_NAME` for custom branding
- Update `VERSION` for release management
- Modify `DESCRIPTION` for API documentation

##### **Server Configuration**
```python
HOST: str = os.getenv("HOST", "127.0.0.1")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
```

**Environment Variables**:
```bash
# Development
export HOST=127.0.0.1
export PORT=8000
export DEBUG=True

# Production
export HOST=0.0.0.0
export PORT=80
export DEBUG=False
```

##### **File Upload Configuration**
```python
MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_FILE_EXTENSIONS: list = [".csv"]
```

**Customization Options**:
```python
# Increase file size limit for large datasets
MAX_FILE_SIZE_MB = 500

# Add support for additional file types
ALLOWED_FILE_EXTENSIONS = [".csv", ".tsv", ".xlsx"]
```

##### **Storage Configuration**
```python
BASE_DIR: Path = Path(__file__).parent.parent
TEMP_FILES_DIR: Path = BASE_DIR / "backend" / "storage" / "temp_files"
DOWNLOADS_DIR: Path = BASE_DIR / "backend" / "storage" / "downloads"
CHROMA_DIR: Path = BASE_DIR / "backend" / "storage" / ".chroma"
FAISS_DIR: Path = BASE_DIR / "backend" / "storage" / ".faiss"
```

**Custom Storage Locations**:
```python
# Use external storage
DOWNLOADS_DIR = Path("/mnt/external/csv_chunker/downloads")
CHROMA_DIR = Path("/var/lib/chromadb")
FAISS_DIR = Path("/var/lib/faiss")
```

##### **Processing Configuration**
```python
DEFAULT_EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
DEFAULT_BATCH_SIZE: int = 32
DEFAULT_TOP_K: int = 5
DEFAULT_SIMILARITY_METRIC: str = "cosine"
```

**Performance Tuning**:
```python
# For high-performance systems
DEFAULT_BATCH_SIZE = 64

# For memory-constrained systems  
DEFAULT_BATCH_SIZE = 16

# Alternative embedding models
DEFAULT_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # Higher quality
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L12-v2"       # Larger model
```

##### **CORS Configuration**
```python
CORS_ORIGINS: list = [
    "http://localhost:3000",
    "http://localhost:8080", 
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*"  # Allow all origins for development
]
```

**Security Considerations**:
```python
# Production CORS (restrictive)
CORS_ORIGINS = [
    "https://your-domain.com",
    "https://app.your-domain.com"
]

# Development CORS (permissive)
CORS_ORIGINS = ["*"]
```

##### **Layer Default Configurations**
```python
LAYER_1_DEFAULTS = {
    "preprocessing": {
        "remove_duplicates": True,
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

**Layer Customization**:
```python
# Fast processing with fixed chunking
LAYER_1_DEFAULTS["chunking"] = {
    "method": "fixed",
    "chunk_size": 100
}

# High-quality processing
LAYER_1_DEFAULTS["embedding"] = {
    "model": "BAAI/bge-small-en-v1.5",
    "batch_size": 64
}

# Production storage
LAYER_1_DEFAULTS["storage"] = {
    "type": "faiss",
    "similarity_metric": "cosine"
}
```

#### **Environment Variable Integration**

##### **Creating .env File**
```bash
# .env file for local development
HOST=127.0.0.1
PORT=8000
DEBUG=True
MAX_FILE_SIZE_MB=200
FILE_RETENTION_HOURS=48
RATE_LIMIT_PER_MINUTE=120

# Database configuration
CHROMA_PERSIST_DIRECTORY=/opt/chromadb
FAISS_INDEX_DIRECTORY=/opt/faiss

# Security settings
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
```

##### **Loading Environment Variables**
```python
# In settings.py
import os
from pathlib import Path

# Load .env file if it exists
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

class Settings:
    # Use environment variables with defaults
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Custom configuration from environment
    CUSTOM_MODEL_PATH: str = os.getenv("CUSTOM_MODEL_PATH", "")
    EXTERNAL_API_KEY: str = os.getenv("EXTERNAL_API_KEY", "")
```

### 📝 Logging Configuration - `config/logging.py`

#### **Logging Setup Structure**
```python
import logging
import logging.handlers
from pathlib import Path

def setup_logging() -> logging.Logger:
    """Configure application logging with file and console handlers"""
    
    # Create logs directory
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            # File handler with rotation
            logging.handlers.RotatingFileHandler(
                log_dir / "app.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            # Console handler
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)
```

#### **Logging Configuration Options**

##### **Log Levels**
```python
# Development logging (verbose)
logging.basicConfig(level=logging.DEBUG)

# Production logging (minimal)
logging.basicConfig(level=logging.WARNING)

# Custom log levels per module
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("chromadb").setLevel(logging.ERROR)
```

##### **Log Formatting**
```python
# Detailed format for debugging
detailed_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

# JSON format for structured logging
import json
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName
        }
        return json.dumps(log_entry)
```

##### **File Rotation**
```python
# Size-based rotation
size_handler = logging.handlers.RotatingFileHandler(
    "app.log",
    maxBytes=50*1024*1024,  # 50MB
    backupCount=10
)

# Time-based rotation
time_handler = logging.handlers.TimedRotatingFileHandler(
    "app.log",
    when="midnight",
    interval=1,
    backupCount=30
)
```

### 🔧 Advanced Configuration

#### **Custom Configuration Classes**
```python
# config/custom_settings.py
from .settings import Settings

class DevelopmentSettings(Settings):
    """Development-specific settings"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    CORS_ORIGINS = ["*"]
    FILE_RETENTION_HOURS = 1  # Quick cleanup for development

class ProductionSettings(Settings):
    """Production-specific settings"""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    CORS_ORIGINS = ["https://your-domain.com"]
    FILE_RETENTION_HOURS = 168  # 7 days
    
    # Production database settings
    CHROMA_DIR = Path("/var/lib/chromadb")
    FAISS_DIR = Path("/var/lib/faiss")

class TestingSettings(Settings):
    """Testing-specific settings"""
    DEBUG = True
    LOG_LEVEL = "ERROR"  # Minimal logging during tests
    TEMP_FILES_DIR = Path("/tmp/csv_chunker_test")
    FILE_RETENTION_HOURS = 0  # Immediate cleanup
```

#### **Configuration Factory**
```python
# config/factory.py
import os
from .custom_settings import DevelopmentSettings, ProductionSettings, TestingSettings

def get_settings():
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()

# Usage in main.py
from config.factory import get_settings
settings = get_settings()
```

#### **Configuration Validation**
```python
# config/validation.py
def validate_settings(settings):
    """Validate configuration settings"""
    errors = []
    
    # Validate required directories
    required_dirs = [
        settings.TEMP_FILES_DIR,
        settings.DOWNLOADS_DIR,
        settings.CHROMA_DIR,
        settings.FAISS_DIR
    ]
    
    for dir_path in required_dirs:
        if not dir_path.parent.exists():
            errors.append(f"Parent directory does not exist: {dir_path.parent}")
    
    # Validate numeric settings
    if settings.MAX_FILE_SIZE_MB <= 0:
        errors.append("MAX_FILE_SIZE_MB must be positive")
    
    if settings.DEFAULT_BATCH_SIZE <= 0:
        errors.append("DEFAULT_BATCH_SIZE must be positive")
    
    # Validate model availability
    try:
        from sentence_transformers import SentenceTransformer
        SentenceTransformer(settings.DEFAULT_EMBEDDING_MODEL)
    except Exception as e:
        errors.append(f"Embedding model not available: {e}")
    
    if errors:
        raise ValueError(f"Configuration errors: {errors}")
    
    return True
```

### 📊 Configuration Management Best Practices

#### **1. Environment Separation**
```bash
# Use different configuration files per environment
config/
├── settings.py          # Base settings
├── development.py       # Development overrides
├── production.py        # Production overrides
├── testing.py          # Testing overrides
└── local.py            # Local developer overrides (gitignored)
```

#### **2. Secret Management**
```python
# Never commit secrets to version control
# Use environment variables or external secret management

# Bad
DATABASE_PASSWORD = "hardcoded_password"

# Good
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
if not DATABASE_PASSWORD:
    raise ValueError("DATABASE_PASSWORD environment variable required")
```

#### **3. Configuration Documentation**
```python
class Settings:
    """
    Application configuration settings
    
    Environment Variables:
        HOST: Server bind address (default: 127.0.0.1)
        PORT: Server port number (default: 8000)
        DEBUG: Enable debug mode (default: False)
        MAX_FILE_SIZE_MB: Maximum upload size in MB (default: 100)
    
    Example:
        export HOST=0.0.0.0
        export PORT=80
        export DEBUG=False
    """
```

#### **4. Configuration Testing**
```python
# test_config.py
def test_default_settings():
    """Test that default settings are valid"""
    from config.settings import Settings
    settings = Settings()
    
    assert settings.HOST == "127.0.0.1"
    assert settings.PORT == 8000
    assert settings.MAX_FILE_SIZE_MB > 0

def test_environment_override():
    """Test environment variable override"""
    import os
    os.environ["PORT"] = "9000"
    
    from config.settings import Settings
    settings = Settings()
    
    assert settings.PORT == 9000
```

This comprehensive configuration documentation covers all aspects of managing settings, dependencies, and environment-specific configurations in CSV Chunker Pro.

