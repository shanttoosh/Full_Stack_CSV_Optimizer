#!/usr/bin/env python3
"""
Fix CORS and start both servers
"""
import subprocess
import time
import requests
import os
import signal
import sys

def kill_existing_processes():
    """Kill any existing Python processes"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                         capture_output=True, text=True)
            print("✅ Killed existing Python processes")
        else:  # Linux/Mac
            subprocess.run(['pkill', '-f', 'python'], 
                         capture_output=True, text=True)
            print("✅ Killed existing Python processes")
    except Exception as e:
        print(f"⚠️ Could not kill processes: {e}")

def start_backend():
    """Start the backend server"""
    try:
        print("🚀 Starting backend server...")
        backend_process = subprocess.Popen(
            [sys.executable, 'scripts/start_server.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for backend to start
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get('http://127.0.0.1:8000/api/v1/health', timeout=2)
                if response.status_code == 200:
                    print("✅ Backend is healthy!")
                    return backend_process
            except:
                pass
            time.sleep(1)
            print(f"⏳ Waiting for backend... ({i+1}/30)")
        
        print("❌ Backend failed to start")
        return None
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the frontend server"""
    try:
        print("🚀 Starting frontend server...")
        frontend_process = subprocess.Popen(
            [sys.executable, 'scripts/start_frontend.py', '--port', '3000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for frontend to start
        for i in range(15):  # Wait up to 15 seconds
            try:
                response = requests.get('http://localhost:3000', timeout=2)
                if response.status_code == 200:
                    print("✅ Frontend is running!")
                    return frontend_process
            except:
                pass
            time.sleep(1)
            print(f"⏳ Waiting for frontend... ({i+1}/15)")
        
        print("✅ Frontend should be running (may not respond to GET)")
        return frontend_process
        
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def test_cors():
    """Test if CORS is working"""
    try:
        print("🧪 Testing CORS...")
        
        # Create a test request similar to what the frontend sends
        import base64
        csv_content = "Name,Age\nJohn,25\nJane,30"
        csv_b64 = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
        
        payload = {
            "csv_data": csv_b64,
            "filename": "test.csv"
        }
        
        response = requests.post(
            'http://127.0.0.1:8000/api/v1/layer1/process',
            json=payload,
            headers={'Origin': 'http://localhost:3000'},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ CORS is working! API responds correctly")
            result = response.json()
            chunking_method = result.get('processing_summary', {}).get('chunking_results', {}).get('method', 'unknown')
            print(f"🎯 Chunking method: {chunking_method}")
            return True
        else:
            print(f"⚠️ API returned status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
        return False

def main():
    print("🔧 Fixing CORS and starting servers...")
    
    # Kill existing processes
    kill_existing_processes()
    time.sleep(2)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Cannot continue without backend")
        return
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Test CORS
    cors_working = test_cors()
    
    if cors_working:
        print("\n🎉 SUCCESS! Both servers are running and CORS is working!")
        print("📋 Access points:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://127.0.0.1:8000/api/docs")
        print("   Health: http://127.0.0.1:8000/api/v1/health")
        print("\n✅ You can now test semantic chunking in the UI!")
        
        # Keep processes running
        try:
            print("\n⏳ Servers running... Press Ctrl+C to stop")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping servers...")
            if backend_process:
                backend_process.terminate()
            if frontend_process:
                frontend_process.terminate()
            print("✅ Servers stopped")
    else:
        print("\n❌ CORS is not working. Check the error messages above.")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()

if __name__ == "__main__":
    main()
