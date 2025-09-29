"""
Development server starter script
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Start the FastAPI development server"""
    try:
        from backend.api.main import run_development_server
        print("🚀 Starting CSV Chunking Optimizer Pro API...")
        print("📖 API Documentation will be available at: http://localhost:8000/api/docs")
        print("🔍 Health Check: http://localhost:8000/api/v1/health")
        print("ℹ️  API Info: http://localhost:8000/api/v1/info")
        print("\n" + "="*60)
        
        run_development_server()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
