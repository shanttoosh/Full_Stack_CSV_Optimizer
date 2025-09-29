#!/usr/bin/env python3
"""
Test the API pipeline step by step
"""
import sys
import os
import base64
import pandas as pd
from io import StringIO

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_api_pipeline():
    """Test each step of the API pipeline"""
    
    try:
        from backend.services.pipeline import ProcessingPipeline
        from backend.utils.validators import validate_csv_data
        from backend.utils.helpers import get_layer_defaults
        
        print("✅ Pipeline imports successful")
        
        # Step 1: Test CSV data preparation (like API does)
        print("\n1️⃣ Testing CSV data preparation...")
        
        simple_csv = "Name,Age\nJohn,25\nJane,30\nBob,35"
        csv_b64 = base64.b64encode(simple_csv.encode('utf-8')).decode('utf-8')
        
        # Decode like the API does
        try:
            csv_data = base64.b64decode(csv_b64).decode('utf-8')
            print(f"✅ Base64 decode successful")
            print(f"CSV content:\n{csv_data}")
        except Exception as e:
            print(f"❌ Base64 decode failed: {e}")
            return False
        
        # Step 2: Test CSV validation
        print("\n2️⃣ Testing CSV validation...")
        
        try:
            df = validate_csv_data(csv_data)
            print(f"✅ CSV validation successful: {df.shape}")
            print(df.head())
        except Exception as e:
            print(f"❌ CSV validation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Step 3: Test settings
        print("\n3️⃣ Testing settings...")
        
        try:
            settings = get_layer_defaults('fast')
            print(f"✅ Settings loaded: {settings}")
        except Exception as e:
            print(f"❌ Settings failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Step 4: Test pipeline initialization
        print("\n4️⃣ Testing pipeline initialization...")
        
        try:
            pipeline = ProcessingPipeline()
            print("✅ Pipeline initialized")
        except Exception as e:
            print(f"❌ Pipeline init failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Step 5: Test full pipeline processing
        print("\n5️⃣ Testing full pipeline processing...")
        
        try:
            import asyncio
            
            async def test_processing():
                result = await pipeline.process_csv(
                    csv_data=csv_data,
                    filename="test.csv",
                    layer_mode="fast"
                )
                return result
            
            result = asyncio.run(test_processing())
            
            if result.get('success'):
                print("✅ Pipeline processing successful!")
                summary = result.get('processing_summary', {})
                chunking = summary.get('chunking_results', {})
                print(f"🔍 Chunking method: {chunking.get('method', 'unknown')}")
                print(f"🔍 Total chunks: {chunking.get('total_chunks', 0)}")
                return True
            else:
                print("❌ Pipeline processing failed")
                print(f"Error: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Pipeline processing failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api_pipeline()
    if success:
        print("\n🎉 API Pipeline works correctly!")
    else:
        print("\n❌ API Pipeline has issues")
