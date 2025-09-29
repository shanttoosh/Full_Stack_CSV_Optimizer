# 4. Setup & Installation

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