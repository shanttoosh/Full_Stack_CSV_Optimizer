#!/usr/bin/env python3
"""
Direct test of semantic chunking without FastAPI
"""
import pandas as pd
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def test_semantic_chunking_direct():
    """Test semantic chunking directly"""
    
    try:
        # Import the chunking module
        from backend.core.chunking import chunk_dataframe, SemanticChunker
        from backend.utils.helpers import get_layer_defaults
        
        print("✅ Imports successful")
        
        # Create test data
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
        
        # Test Layer 1 defaults
        settings = get_layer_defaults('fast')
        print(f"✅ Layer 1 defaults: {settings}")
        
        chunking_settings = settings.get('chunking', {})
        method = chunking_settings.get('method', 'fixed')
        n_clusters = chunking_settings.get('n_clusters', 5)
        
        print(f"🔍 Chunking method: {method}")
        print(f"🔍 Number of clusters: {n_clusters}")
        
        if method == 'semantic':
            print("🚀 Testing semantic chunking directly...")
            
            # Test direct semantic chunking
            try:
                result = chunk_dataframe(df, method='semantic', n_clusters=n_clusters)
                print(f"✅ Semantic chunking successful!")
                print(f"📊 Method: {result.method}")
                print(f"📊 Total chunks: {result.total_chunks}")
                print(f"📊 Quality: {result.quality_report.get('overall_quality', 'N/A')}")
                
                # Check first chunk metadata
                if result.metadata:
                    first_metadata = result.metadata[0]
                    print(f"📊 First chunk metadata: {first_metadata.extra_metadata}")
                
                return True
                
            except Exception as e:
                print(f"❌ Semantic chunking failed: {e}")
                import traceback
                traceback.print_exc()
                return False
        else:
            print(f"❌ Settings still show method: {method} instead of semantic")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_semantic_chunking_direct()
    if success:
        print("\n🎉 DIRECT SEMANTIC CHUNKING WORKS!")
    else:
        print("\n❌ Direct semantic chunking failed")
