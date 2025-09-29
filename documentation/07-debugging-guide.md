# 7. Debugging Guide

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