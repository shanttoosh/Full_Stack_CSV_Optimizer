# 12. Configuration Files

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