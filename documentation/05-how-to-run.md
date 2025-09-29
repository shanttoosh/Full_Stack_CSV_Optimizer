# 5. How to Run

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