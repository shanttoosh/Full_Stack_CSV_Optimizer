#!/usr/bin/env python3
"""
Debug the 500 error in the API
"""
import requests
import json
import base64

def debug_api():
    """Debug the API error"""
    
    print("🔍 Debugging API 500 Error")
    print("=" * 40)
    
    # Very simple test data
    simple_csv = "Name,Age\nJohn,25\nJane,30\nBob,35"
    csv_b64 = base64.b64encode(simple_csv.encode('utf-8')).decode('utf-8')
    
    payload = {
        "csv_data": csv_b64,
        "filename": "simple_test.csv"
    }
    
    print("📝 Testing with simple 3-row CSV...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/layer1/process",
            json=payload,
            timeout=30
        )
        
        print(f"🔍 Status Code: {response.status_code}")
        print(f"🔍 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 500:
            print("❌ Internal Server Error Details:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(f"Raw response: {response.text}")
        elif response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            if 'processing_summary' in result:
                chunking = result['processing_summary'].get('chunking_results', {})
                print(f"🔍 Chunking method: {chunking.get('method', 'unknown')}")
        else:
            print(f"⚠️ Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    debug_api()
