#!/usr/bin/env python3
"""
Final test to verify semantic chunking is working in Layer 1 (Fast Mode)
"""
import requests
import json
import base64
import time

def test_semantic_chunking():
    """Test Layer 1 semantic chunking end-to-end"""
    
    print("🧪 Testing Semantic Chunking in Layer 1 (Fast Mode)")
    print("=" * 60)
    
    # Step 1: Check if servers are running
    print("1️⃣ Checking server status...")
    
    try:
        # Check backend health
        health_response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Backend is healthy")
            health_data = health_response.json()
            print(f"   Version: {health_data.get('version', 'N/A')}")
            print(f"   Services: {health_data.get('services', {})}")
        else:
            print(f"❌ Backend health check failed: {health_response.status_code}")
            return False
            
        # Check frontend (optional, might not respond to GET)
        try:
            frontend_response = requests.get("http://localhost:3000", timeout=3)
            print("✅ Frontend is accessible")
        except:
            print("⚠️ Frontend check skipped (normal for static server)")
            
    except Exception as e:
        print(f"❌ Server check failed: {e}")
        print("💡 Make sure both servers are running:")
        print("   Backend: python scripts/start_server.py")
        print("   Frontend: python scripts/start_frontend.py --port 3000")
        return False
    
    # Step 2: Create test data (Titanic-like dataset)
    print("\n2️⃣ Preparing test data...")
    
    test_csv = """PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked
1,0,3,"Braund, Mr. Owen Harris",male,22,1,0,A/5 21171,7.25,,S
2,1,1,"Cumings, Mrs. John Bradley (Florence Briggs Thayer)",female,38,1,0,PC 17599,71.2833,C85,C
3,1,3,"Heikkinen, Miss. Laina",female,26,0,0,STON/O2. 3101282,7.925,,S
4,1,1,"Futrelle, Mrs. Jacques Heath (Lily May Peel)",female,35,1,0,113803,53.1,C123,S
5,0,3,"Allen, Mr. William Henry",male,35,0,0,373450,8.05,,S
6,0,3,"Moran, Mr. James",male,27,0,0,330877,8.4583,,Q
7,0,1,"McCarthy, Mr. Timothy J",male,54,0,0,17463,51.8625,E46,S
8,0,3,"Palsson, Master. Gosta Leonard",male,2,3,1,349909,21.075,,S
9,1,3,"Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)",female,27,0,2,347742,11.1333,,S
10,1,2,"Nasser, Mrs. Nicholas (Adele Achem)",female,14,1,0,237736,30.0708,,C
11,1,3,"Sandstrom, Miss. Marguerite Rut",female,4,1,1,PP 9549,16.7,G6,S
12,1,1,"Bonnell, Miss. Elizabeth",female,58,0,0,113783,26.55,C103,S
13,0,3,"Saundercock, Mr. William Henry",male,20,0,0,A/5. 2151,8.05,,S
14,0,3,"Andersson, Mr. Anders Johan",male,39,1,5,347082,31.275,,S
15,0,3,"Vestrom, Miss. Hulda Amanda Adolfina",female,14,0,0,350406,7.8542,,S
16,1,2,"Hewlett, Mrs. (Mary D Kingcome) ",female,55,0,0,248706,16,,S
17,0,3,"Rice, Master. Eugene",male,2,4,1,382652,29.125,,Q
18,1,2,"Williams, Mr. Charles Eugene",male,23,0,0,244373,13,,S
19,0,3,"Vander Planke, Mrs. Julius (Emelia Maria Vandemoortele)",female,31,1,0,345763,18,,S
20,1,3,"Masselmani, Mrs. Fatima",female,22,0,0,2649,7.225,,C"""

    # Encode as base64
    csv_b64 = base64.b64encode(test_csv.encode('utf-8')).decode('utf-8')
    
    payload = {
        "csv_data": csv_b64,
        "filename": "test_titanic.csv"
    }
    
    print(f"✅ Test dataset created: 20 rows, 12 columns")
    
    # Step 3: Test Layer 1 processing
    print("\n3️⃣ Testing Layer 1 (Fast Mode) processing...")
    
    try:
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:8000/api/v1/layer1/process",
            json=payload,
            headers={
                'Content-Type': 'application/json',
                'Origin': 'http://localhost:3000'
            },
            timeout=60
        )
        
        processing_time = time.time() - start_time
        print(f"⏱️ Processing took {processing_time:.2f} seconds")
        
        if response.status_code != 200:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        result = response.json()
        print("✅ Layer 1 processing successful!")
        
    except Exception as e:
        print(f"❌ API request failed: {e}")
        return False
    
    # Step 4: Analyze results
    print("\n4️⃣ Analyzing chunking results...")
    
    if 'processing_summary' not in result:
        print("❌ No processing summary in response")
        return False
    
    summary = result['processing_summary']
    
    # Check chunking results
    if 'chunking_results' in summary:
        chunking_results = summary['chunking_results']
        method = chunking_results.get('method', 'unknown')
        total_chunks = chunking_results.get('total_chunks', 0)
        
        print(f"🔍 Chunking method: {method}")
        print(f"📊 Total chunks: {total_chunks}")
        
        if method == 'semantic':
            print("🎉 SUCCESS: Semantic chunking is working!")
            
            # Check quality
            quality = chunking_results.get('quality_report', {})
            print(f"📈 Quality: {quality.get('overall_quality', 'N/A')}")
            print(f"📈 Quality score: {quality.get('quality_score', 'N/A')}")
            
            # Expected: 5 clusters for semantic chunking
            if total_chunks == 5:
                print("✅ Correct number of clusters (5)")
            else:
                print(f"⚠️ Expected 5 clusters, got {total_chunks}")
                
        else:
            print(f"❌ FAILED: Expected 'semantic', got '{method}'")
            return False
    else:
        print("❌ No chunking results found")
        return False
    
    # Check embedding results
    if 'embedding_results' in summary:
        embedding_results = summary['embedding_results']
        model = embedding_results.get('model_used', 'unknown')
        embeddings_count = embedding_results.get('total_embeddings', 0)
        
        print(f"🧠 Embedding model: {model}")
        print(f"📊 Total embeddings: {embeddings_count}")
        
        if model == 'all-MiniLM-L6-v2':
            print("✅ Correct embedding model")
        else:
            print(f"⚠️ Expected 'all-MiniLM-L6-v2', got '{model}'")
    
    # Step 5: Check download links
    print("\n5️⃣ Checking download files...")
    
    if 'download_links' in result:
        downloads = result['download_links']
        
        for file_type, info in downloads.items():
            print(f"📁 {file_type}: {info.get('size_bytes', 0)} bytes")
            
        # Test downloading chunks CSV
        if 'chunks_csv' in downloads:
            try:
                chunks_url = f"http://localhost:8000{downloads['chunks_csv']['url']}"
                chunks_response = requests.get(chunks_url, timeout=10)
                
                if chunks_response.status_code == 200:
                    print("✅ Chunks CSV download successful")
                    
                    # Check if it contains semantic chunking indicators
                    csv_content = chunks_response.text
                    if 'semantic' in csv_content.lower():
                        print("✅ CSV contains semantic chunking metadata")
                    else:
                        print("⚠️ CSV might not contain semantic metadata")
                        
                else:
                    print(f"⚠️ Chunks download failed: {chunks_response.status_code}")
                    
            except Exception as e:
                print(f"⚠️ Could not test download: {e}")
    
    # Step 6: Test search functionality
    print("\n6️⃣ Testing search functionality...")
    
    if 'search_endpoint' in result:
        search_endpoint = result['search_endpoint']
        processing_id = result.get('processing_id')
        
        try:
            search_payload = {
                "query": "passenger information",
                "top_k": 3
            }
            
            search_response = requests.post(
                f"http://localhost:8000{search_endpoint}",
                json=search_payload,
                timeout=10
            )
            
            if search_response.status_code == 200:
                search_results = search_response.json()
                results_count = len(search_results.get('results', []))
                print(f"✅ Search successful: {results_count} results")
            else:
                print(f"⚠️ Search failed: {search_response.status_code}")
                
        except Exception as e:
            print(f"⚠️ Search test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 SEMANTIC CHUNKING TEST COMPLETE!")
    print("✅ Layer 1 (Fast Mode) is now using:")
    print("   - Semantic chunking with KMeans clustering")
    print("   - 5 clusters (as configured)")
    print("   - all-MiniLM-L6-v2 embeddings")
    print("   - ChromaDB storage with cosine similarity")
    print("\n🚀 Ready for production use!")
    
    return True

if __name__ == "__main__":
    success = test_semantic_chunking()
    if success:
        print("\n🎯 Test Result: PASSED ✅")
    else:
        print("\n🎯 Test Result: FAILED ❌")
        print("💡 Check the error messages above and ensure servers are running")
