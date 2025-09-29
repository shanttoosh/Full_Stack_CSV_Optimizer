"""
Quick test for FastAPI imports and basic functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test all imports work correctly"""
    print("🧪 Testing FastAPI imports...")
    
    try:
        # Test config imports
        from config.settings import settings
        print("✅ Config imports: OK")
        
        # Test API imports
        from backend.api.models import ProcessResponse, Layer1ProcessRequest
        print("✅ API models: OK")
        
        # Test service imports
        from backend.services.pipeline import ProcessingPipeline
        from backend.services.file_handler import FileHandler
        from backend.services.response_builder import ResponseBuilder
        print("✅ Services: OK")
        
        # Test route imports
        from backend.api.routes.layer_routes import router as layer_router
        from backend.api.routes.unified_routes import router as unified_router
        print("✅ Routes: OK")
        
        # Test FastAPI app creation
        from fastapi import FastAPI
        app = FastAPI(title="Test App")
        print("✅ FastAPI app creation: OK")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test settings
        from config.settings import settings
        print(f"✅ Settings loaded: {settings.APP_NAME}")
        
        # Test pipeline creation
        from backend.services.pipeline import ProcessingPipeline
        pipeline = ProcessingPipeline()
        print("✅ Pipeline creation: OK")
        
        # Test file handler
        from backend.services.file_handler import FileHandler
        file_handler = FileHandler()
        print("✅ File handler: OK")
        
        # Test response builder
        from backend.services.response_builder import ResponseBuilder
        response_builder = ResponseBuilder()
        health_response = response_builder.build_health_response()
        print(f"✅ Response builder: OK (Status: {health_response['status']})")
        
        print("\n🎉 Basic functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 FastAPI Integration Test")
    print("=" * 50)
    
    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    
    print("\n" + "=" * 50)
    if imports_ok and functionality_ok:
        print("✅ FastAPI integration is ready!")
        print("\n🚀 To start the server, run:")
        print("   python scripts/start_server.py")
        print("\n📖 API Documentation will be at:")
        print("   http://localhost:8000/api/docs")
    else:
        print("❌ FastAPI integration has issues")
        print("   Please fix the errors above before starting the server")

if __name__ == "__main__":
    main()

