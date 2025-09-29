# 8. Error Handling Matrix

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