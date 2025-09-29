# 2. Project Structure

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
