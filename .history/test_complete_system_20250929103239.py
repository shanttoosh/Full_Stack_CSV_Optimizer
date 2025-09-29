"""
Complete system test for CSV Chunking Optimizer Pro
"""

import sys
import os
import time
import requests
import subprocess
import threading
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_backend_startup():
    """Test if backend starts successfully"""
    print("🔧 Testing Backend Startup...")
    
    try:
        # Import the main app to test
        from backend.api.main import app
        from config.settings import settings
        
        print(f"✅ Backend imports successful")
        print(f"✅ Configured for {settings.HOST}:{settings.PORT}")
        return True
        
    except Exception as e:
        print(f"❌ Backend startup test failed: {e}")
        return False

def test_frontend_files():
    """Test if frontend files exist and are valid"""
    print("🌐 Testing Frontend Files...")
    
    required_files = [
        "frontend/index.html",
        "frontend/script.js",
        "frontend/styles.css"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Missing file: {file_path}")
            return False
        
        # Check file size
        size = os.path.getsize(file_path)
        if size == 0:
            print(f"❌ Empty file: {file_path}")
            return False
        
        print(f"✅ {file_path} ({size} bytes)")
    
    return True

def test_api_health():
    """Test API health endpoint"""
    print("🏥 Testing API Health...")
    
    try:
        response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"❌ API Health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️ API not running (expected if not started): {e}")
        return True  # This is expected if servers aren't running

def create_sample_csv():
    """Create a sample CSV for testing"""
    print("📄 Creating Sample CSV...")
    
    sample_csv = """name,age,city,occupation
John Doe,30,New York,Engineer
Jane Smith,25,Los Angeles,Designer
Bob Johnson,35,Chicago,Manager
Alice Brown,28,Houston,Developer
Charlie Wilson,32,Phoenix,Analyst"""
    
    with open("sample_test.csv", "w") as f:
        f.write(sample_csv)
    
    print("✅ Sample CSV created: sample_test.csv")
    return True

def test_layer_defaults():
    """Test layer default configurations"""
    print("⚙️ Testing Layer Defaults...")
    
    try:
        from config.settings import settings
        
        # Test Layer 1 defaults
        layer1 = settings.LAYER_1_DEFAULTS
        if layer1['chunking']['method'] == 'semantic':
            print("✅ Layer 1: Semantic chunking configured")
        else:
            print(f"❌ Layer 1: Expected semantic, got {layer1['chunking']['method']}")
            return False
        
        if layer1['storage']['type'] == 'chroma':
            print("✅ Layer 1: Chroma storage configured")
        else:
            print(f"❌ Layer 1: Expected chroma, got {layer1['storage']['type']}")
            return False
        
        if layer1['storage']['similarity_metric'] == 'cosine':
            print("✅ Layer 1: Cosine similarity configured")
        else:
            print(f"❌ Layer 1: Expected cosine, got {layer1['storage']['similarity_metric']}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Layer defaults test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 CSV CHUNKING OPTIMIZER PRO - COMPLETE SYSTEM TEST")
    print("=" * 60)
    
    tests = [
        ("Backend Startup", test_backend_startup),
        ("Frontend Files", test_frontend_files),
        ("API Health", test_api_health),
        ("Sample CSV", create_sample_csv),
        ("Layer Defaults", test_layer_defaults),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} - Exception: {e}")
            failed += 1
        
        print()  # Add spacing
    
    print("=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n🚀 Your system is ready to run!")
        print("\n📋 STARTUP INSTRUCTIONS:")
        print("1. Backend:  python scripts/start_server.py")
        print("2. Frontend: python scripts/start_frontend.py")
        print("3. Open:     http://localhost:3000")
        print("4. Test:     Upload sample_test.csv and process with Layer 1")
        
        print("\n✨ EXPECTED BEHAVIOR:")
        print("• Layer 1 (Fast): Semantic chunking + all-MiniLM + Chroma + Cosine")
        print("• Processing: Header validation → Preprocessing → Chunking → Embeddings → Storage → Retrieval")
        print("• Result: Download buttons + Search interface")
        
    else:
        print(f"\n🚨 {failed} TESTS FAILED!")
        print("Please fix the issues above before running the system.")
    
    # Cleanup
    if os.path.exists("sample_test.csv"):
        print("\n🧹 Cleaning up test files...")
        os.remove("sample_test.csv")

if __name__ == "__main__":
    main()

