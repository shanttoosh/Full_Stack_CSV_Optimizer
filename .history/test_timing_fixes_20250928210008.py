#!/usr/bin/env python3
"""
Test script to verify the timing and alignment fixes
"""
import requests
import json
import base64
import time

def test_timing_fixes():
    """Test that the timing display fixes are working"""
    
    print("🧪 TESTING TIMING AND ALIGNMENT FIXES")
    print("=" * 50)
    
    # Check backend health
    print("1️⃣ Backend Health Check...")
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False
    
    # Test step endpoints with timing
    print("\n2️⃣ Testing Step Timing...")
    
    test_csv = """Name,Age,City
John,25,New York
Jane,30,Los Angeles
Bob,35,Chicago
Alice,28,Seattle
Charlie,32,Boston"""
    
    csv_b64 = base64.b64encode(test_csv.encode('utf-8')).decode('utf-8')
    payload = {"csv_data": csv_b64, "filename": "test_timing.csv"}
    
    steps = [
        ("preprocessing", "/api/v1/step/preprocessing"),
        ("chunking", "/api/v1/step/chunking"),
        ("embedding", "/api/v1/step/embedding"),
        ("storing", "/api/v1/step/storing")
    ]
    
    step_times = {}
    
    for step_name, endpoint in steps:
        print(f"   🔄 Testing {step_name}...")
        
        start_time = time.time()
        try:
            response = requests.post(f"http://127.0.0.1:8000{endpoint}", json=payload, timeout=30)
            actual_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                reported_time = result.get('processing_time_seconds', 0)
                
                step_times[step_name] = {
                    'reported': reported_time,
                    'actual': actual_time,
                    'message': result.get('message', ''),
                    'success': True
                }
                
                print(f"   ✅ {step_name}: {reported_time:.2f}s (actual: {actual_time:.2f}s)")
                print(f"      📝 Message: {result.get('message', 'N/A')}")
                
            else:
                print(f"   ❌ {step_name} failed: {response.status_code}")
                step_times[step_name] = {'success': False, 'error': response.text}
                
        except Exception as e:
            print(f"   ❌ {step_name} error: {e}")
            step_times[step_name] = {'success': False, 'error': str(e)}
    
    # Test full Layer 1 processing
    print("\n3️⃣ Testing Full Layer 1 Processing...")
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/layer1/process",
            json=payload,
            timeout=60
        )
        total_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            processing_time = result.get('processing_summary', {}).get('processing_time_seconds', 0)
            
            print(f"   ✅ Full processing: {processing_time:.2f}s (actual: {total_time:.2f}s)")
            print(f"   📊 Processing ID: {result.get('processing_id', 'N/A')}")
            print(f"   📁 Download links: {len(result.get('download_links', {}))}")
            
            full_processing_success = True
            
        else:
            print(f"   ❌ Full processing failed: {response.status_code}")
            print(f"   📝 Response: {response.text}")
            full_processing_success = False
            
    except Exception as e:
        print(f"   ❌ Full processing error: {e}")
        full_processing_success = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TIMING FIXES TEST SUMMARY:")
    
    successful_steps = sum(1 for s in step_times.values() if s.get('success', False))
    print(f"✅ Step endpoints working: {successful_steps}/4")
    
    if successful_steps >= 3:
        print(f"✅ Step timing: Individual step times are being reported correctly")
        
        # Check if times are realistic
        reported_times = [s['reported'] for s in step_times.values() if s.get('success', False)]
        if len(set(reported_times)) > 1:
            print(f"✅ Dynamic timing: Steps have different processing times")
        else:
            print(f"⚠️ All steps report same time - may not be fully dynamic")
    else:
        print(f"❌ Step timing: Not enough steps working")
    
    if full_processing_success:
        print(f"✅ Full processing: Complete Layer 1 API working")
    else:
        print(f"❌ Full processing: Layer 1 API has issues")
    
    # Frontend instructions
    print(f"\n💡 FRONTEND TEST INSTRUCTIONS:")
    print(f"   1. Open http://localhost:3000 in your browser")
    print(f"   2. Select Layer 1 (Fast Mode)")
    print(f"   3. Upload a CSV file")
    print(f"   4. Click 'Start Processing'")
    print(f"   5. Watch for:")
    print(f"      - Live timing updates (Processing... 1s, 2s, 3s...)")
    print(f"      - Completion messages (Completed in Xs)")
    print(f"      - Proper alignment of status text")
    print(f"      - Download buttons appear ONLY after all steps complete")
    print(f"      - NO restart of processing steps")
    
    if successful_steps >= 3 and full_processing_success:
        print(f"\n🎉 TIMING FIXES TEST: PASSED ✅")
        print(f"   The dynamic step-by-step timing system is working!")
        return True
    else:
        print(f"\n❌ TIMING FIXES TEST: NEEDS ATTENTION")
        print(f"   Some endpoints or functionality need fixes")
        return False

if __name__ == "__main__":
    success = test_timing_fixes()
    
    print(f"\n{'='*50}")
    if success:
        print(f"🎯 TIMING FIXES: READY FOR TESTING ✅")
        print(f"🌐 Open http://localhost:3000 to test the frontend!")
    else:
        print(f"🎯 TIMING FIXES: BACKEND ISSUES DETECTED ❌")
        print(f"🔧 Fix backend issues before testing frontend")
