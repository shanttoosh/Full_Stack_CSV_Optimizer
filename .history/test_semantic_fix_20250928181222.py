#!/usr/bin/env python3
"""
Quick test to verify semantic chunking fix
"""
import requests
import json
import time

def test_semantic_chunking():
    """Test if Layer 1 now uses semantic chunking"""
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test health endpoint
        health_response = requests.get("http://127.0.0.1:8000/api/v1/health")
        if health_response.status_code != 200:
            print("❌ Server not ready")
            return False
            
        print("✅ Server is healthy")
        
        # Test Layer 1 defaults
        # Create a simple CSV content
        csv_content = """PassengerId,Survived,Pclass,Name,Sex,Age
1,0,3,"Braund, Mr. Owen Harris",male,22
2,1,1,"Cumings, Mrs. John Bradley",female,38
3,1,3,"Heikkinen, Miss. Laina",female,26
4,1,1,"Futrelle, Mrs. Jacques Heath",female,35
5,0,3,"Allen, Mr. William Henry",male,35
6,0,3,"Moran, Mr. James",male,27
7,0,1,"McCarthy, Mr. Timothy J",male,54
8,0,3,"Palsson, Master. Gosta Leonard",male,2
9,1,3,"Johnson, Mrs. Oscar W",female,27
10,1,2,"Nasser, Mrs. Nicholas",female,14"""
        
        # Test Layer 1 processing
        files = {'file': ('test.csv', csv_content, 'text/csv')}
        data = {'layer': '1'}
        
        print("🚀 Testing Layer 1 processing...")
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/layer1/process",
            files=files,
            data=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Layer 1 processing successful!")
            
            # Check if semantic chunking was used
            if 'processing_summary' in result:
                summary = result['processing_summary']
                if 'chunking_settings' in summary:
                    chunking_method = summary['chunking_settings'].get('method', 'unknown')
                    print(f"🔍 Chunking method used: {chunking_method}")
                    
                    if chunking_method == 'semantic':
                        print("🎉 SUCCESS: Semantic chunking is now working!")
                        return True
                    else:
                        print(f"❌ FAILED: Still using {chunking_method} instead of semantic")
                        return False
                else:
                    print("⚠️ No chunking settings found in response")
                    print(f"Response keys: {list(result.keys())}")
                    return False
            else:
                print("⚠️ No processing summary found in response")
                print(f"Response keys: {list(result.keys())}")
                return False
        else:
            print(f"❌ Layer 1 processing failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_semantic_chunking()
    if success:
        print("\n🎉 SEMANTIC CHUNKING FIX VERIFIED!")
    else:
        print("\n❌ Semantic chunking fix needs more work")
