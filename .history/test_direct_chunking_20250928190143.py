#!/usr/bin/env python3
"""
Test chunking directly to isolate the issue
"""
import sys
import os
import pandas as pd
import asyncio
from functools import partial

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

async def test_chunking():
    """Test chunking directly"""
    
    try:
        from backend.core.chunking import chunk_dataframe
        from config.settings import Settings
        
        print("✅ Imports successful")
        
        # Create test data
        data = {
            'Name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
            'Age': [25, 30, 35, 28, 32],
            'City': ['NY', 'LA', 'Chicago', 'Boston', 'Seattle']
        }
        
        df = pd.DataFrame(data)
        print(f"✅ Test DataFrame: {df.shape}")
        print(df.head())
        
        # Get settings
        settings_obj = Settings()
        chunking_settings = settings_obj.LAYER_1_DEFAULTS.get('chunking', {})
        method = chunking_settings.get('method', 'fixed')
        method_params = {k: v for k, v in chunking_settings.items() if k != "method"}
        
        print(f"🔍 Method: {method}")
        print(f"🔍 Params: {method_params}")
        
        # Test direct call
        print("🧪 Testing direct call...")
        try:
            result = chunk_dataframe(df, method, **method_params)
            print(f"✅ Direct call successful: {result.method}, {result.total_chunks} chunks")
        except Exception as e:
            print(f"❌ Direct call failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test async executor call (like pipeline does)
        print("🧪 Testing async executor call...")
        try:
            loop = asyncio.get_event_loop()
            chunk_func = partial(chunk_dataframe, df, method, **method_params)
            result = await loop.run_in_executor(None, chunk_func)
            print(f"✅ Async call successful: {result.method}, {result.total_chunks} chunks")
            return True
        except Exception as e:
            print(f"❌ Async call failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_chunking())
    if success:
        print("\n🎉 Chunking works correctly!")
    else:
        print("\n❌ Chunking has issues")
