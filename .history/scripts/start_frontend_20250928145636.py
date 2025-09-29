"""
Simple HTTP server to serve the frontend files
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

def start_frontend_server(port=3000):
    """Start frontend development server"""
    
    # Change to frontend directory
    frontend_dir = Path(__file__).parent.parent / "frontend"
    os.chdir(frontend_dir)
    
    # Create handler
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Add CORS headers
    class CORSRequestHandler(Handler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
        
        def do_OPTIONS(self):
            self.send_response(200)
            self.end_headers()
    
    try:
        with socketserver.TCPServer(("", port), CORSRequestHandler) as httpd:
            print(f"🌐 Frontend server starting...")
            print(f"📱 Frontend URL: http://localhost:{port}")
            print(f"🔗 API URL: http://localhost:8000")
            print(f"📖 API Docs: http://localhost:8000/api/docs")
            print("\n" + "="*60)
            print("🚀 Your frontend is now DYNAMIC and connected to the API!")
            print("   - Upload a CSV file")
            print("   - Select processing layer (1, 2, or 3)")  
            print("   - Click 'Start Processing' to use real API")
            print("   - Download real processed files")
            print("   - Search through real data")
            print("="*60)
            print(f"\n🛑 Press Ctrl+C to stop the server")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use")
            print(f"   Try: python scripts/start_frontend.py --port 3001")
        else:
            print(f"❌ Server error: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="CSV Chunking Optimizer Pro - Frontend Server")
    parser.add_argument("--port", type=int, default=3000, help="Port to run frontend server on")
    
    args = parser.parse_args()
    
    start_frontend_server(args.port)

if __name__ == "__main__":
    main()
