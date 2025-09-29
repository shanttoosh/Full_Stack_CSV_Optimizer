# 1. Project Overview

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
