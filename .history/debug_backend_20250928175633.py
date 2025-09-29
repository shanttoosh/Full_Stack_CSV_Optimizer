"""
Debug script to test backend processing directly
"""

import asyncio
import sys
import os
import base64
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_backend():
    """Test backend processing directly"""
    
    # Create sample CSV data (Titanic-like)
    sample_csv = """PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Ticket,Fare,Cabin,Embarked
1,0,3,"Braund, Mr. Owen Harris",male,22,1,0,A/5 21171,7.25,,S
2,1,1,"Cumings, Mrs. John Bradley (Florence Briggs Thayer)",female,38,1,0,PC 17599,71.2833,C85,C
3,1,3,"Heikkinen, Miss. Laina",female,26,0,0,STON/O2. 3101282,7.925,,S
4,1,1,"Futrelle, Mrs. Jacques Heath (Lily May Peel)",female,35,1,0,113803,53.1,C123,S
5,0,3,"Allen, Mr. William Henry",male,35,0,0,373450,8.05,,S"""
    
    # Encode as base64
    csv_base64 = base64.b64encode(sample_csv.encode('utf-8')).decode('utf-8')
    
    print("🧪 Testing backend processing directly...")
    
    try:
        from backend.services.pipeline import ProcessingPipeline
        
        pipeline = ProcessingPipeline()
        
        result = await pipeline.process_csv(
            csv_data=csv_base64,
            filename="test_titanic.csv",
            layer_mode="fast"
        )
        
        print("✅ Backend processing result:")
        print(f"   Success: {result.get('success')}")
        print(f"   Processing ID: {result.get('processing_id')}")
        print(f"   Message: {result.get('message')}")
        
        if result.get('processing_summary'):
            summary = result['processing_summary']
            print(f"   Input rows: {summary.get('input_data', {}).get('total_rows', 'N/A')}")
            print(f"   Chunks: {summary.get('chunking_results', {}).get('total_chunks', 'N/A')}")
            print(f"   Embeddings: {summary.get('embedding_results', {}).get('total_embeddings', 'N/A')}")
        
        if result.get('download_links'):
            print(f"   Download links: {list(result['download_links'].keys())}")
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_backend())
