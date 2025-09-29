"""
Start both FastAPI backend and frontend server
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_full_stack():
    """Start both backend and frontend servers"""
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🚀 Starting CSV Chunking Optimizer Pro - Full Stack")
    print("=" * 60)
    
    try:
        # Start FastAPI backend
        print("🔧 Starting FastAPI backend...")
        backend_process = subprocess.Popen([
            sys.executable, "scripts/start_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start frontend server
        print("🌐 Starting frontend server...")
        frontend_process = subprocess.Popen([
            sys.executable, "scripts/start_frontend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        print("\n" + "=" * 60)
        print("✅ Full Stack Started Successfully!")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📖 API Docs: http://localhost:8000/api/docs")
        print("=" * 60)
        print("\n🎉 Your frontend is now DYNAMIC!")
        print("   - Connected to real FastAPI backend")
        print("   - Real CSV processing")
        print("   - Real file downloads")
        print("   - Real search functionality")
        print("\n🛑 Press Ctrl+C to stop both servers")
        
        # Wait for processes
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            pass
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        
        # Terminate processes
        try:
            backend_process.terminate()
            frontend_process.terminate()
            
            # Wait for clean shutdown
            backend_process.wait(timeout=5)
            frontend_process.wait(timeout=5)
            
        except:
            # Force kill if needed
            try:
                backend_process.kill()
                frontend_process.kill()
            except:
                pass
        
        print("✅ Servers stopped")
    
    except Exception as e:
        print(f"❌ Error starting servers: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_full_stack()
