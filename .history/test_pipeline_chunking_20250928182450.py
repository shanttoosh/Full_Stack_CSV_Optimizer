#!/usr/bin/env python3
"""
Test the exact chunking flow that the pipeline uses
"""
import pandas as pd
import sys
import os
import asyncio

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

async def test_pipeline_chunking():
    """Test the exact chunking flow from pipeline"""
    
    try:
        from backend.core.chunking import chunk_dataframe
        from config.settings import Settings
        
        print("✅ Imports successful")
        
        # Create test data (same as in our test)
        data = {
            'PassengerId': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'Survived': [0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            'Pclass': [3, 1, 3, 1, 3, 3, 1, 3, 3, 2],
            'Name': [
                "Braund, Mr. Owen Harris",
                "Cumings, Mrs. John Bradley", 
                "Heikkinen, Miss. Laina",
                "Futrelle, Mrs. Jacques Heath",
                "Allen, Mr. William Henry",
                "Moran, Mr. James",
                "McCarthy, Mr. Timothy J",
                "Palsson, Master. Gosta Leonard",
                "Johnson, Mrs. Oscar W",
                "Nasser, Mrs. Nicholas"
            ],
            'Sex': ['male', 'female', 'female', 'female', 'male', 'male', 'male', 'male', 'female', 'female'],
            'Age': [22, 38, 26, 35, 35, 27, 54, 2, 27, 14]
        }
        
        df = pd.DataFrame(data)
        print(f"✅ Test DataFrame created: {df.shape}")
        
        # Get settings exactly like pipeline does
        settings_obj = Settings()
        layer1_defaults = settings_obj.LAYER_1_DEFAULTS
        print(f"✅ Layer 1 defaults from config: {layer1_defaults}")
        
        chunking_settings = layer1_defaults.get('chunking', {})
        method = chunking_settings.get('method', 'fixed')
        print(f"🔍 Method from settings: {method}")
        
        # Extract method-specific parameters exactly like pipeline does
        method_params = {k: v for k, v in chunking_settings.items() if k != "method"}
        print(f"🔍 Method params: {method_params}")
        
        # Test in executor like pipeline does
        print("🚀 Testing chunking in thread pool executor...")
        
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                None,
                chunk_dataframe,
                df,
                method,
                **method_params
            )
            print(f"✅ Chunking successful!")
            print(f"📊 Method: {result.method}")
            print(f"📊 Total chunks: {result.total_chunks}")
            print(f"📊 Quality: {result.quality_report.get('overall_quality', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Chunking failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_pipeline_chunking())
    if success:
        print("\n🎉 PIPELINE CHUNKING WORKS!")
    else:
        print("\n❌ Pipeline chunking failed")
