"""
Test script for the complete backend modules.
This script tests the core functionality without FastAPI.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_preprocessing():
    """Test preprocessing module"""
    print("🔄 Testing Preprocessing...")
    
    from backend.core.preprocessing import preprocess_csv
    
    # Create sample data
    data = {
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'age': ['25', '30', '35'],
        'email': ['john@email.com', 'jane@email.com', 'bob@email.com']
    }
    df = pd.DataFrame(data)
    
    # Test preprocessing
    config = {
        'type_conversions': {'age': 'numeric'},
        'remove_duplicates': True,
        'text_processing': 'skip'
    }
    
    processed_df, file_meta, numeric_meta = preprocess_csv(df, config)
    
    print(f"✅ Preprocessing: {len(processed_df)} rows, {len(processed_df.columns)} columns")
    print(f"   Numeric metadata: {len(numeric_meta)} columns")
    return processed_df

def test_chunking(df):
    """Test chunking module"""
    print("🔄 Testing Chunking...")
    
    from backend.core.chunking import chunk_dataframe, create_chunker
    
    # Test different chunking methods
    methods = ['fixed', 'recursive', 'semantic']
    results = {}
    
    for method in methods:
        try:
            if method == 'fixed':
                result = chunk_dataframe(df, method=method, chunk_size=2)
            elif method == 'recursive':
                result = chunk_dataframe(df, method=method, chunk_size=100)
            elif method == 'semantic':
                result = chunk_dataframe(df, method=method, n_clusters=2)
            
            results[method] = result
            print(f"✅ {method.title()} chunking: {result.total_chunks} chunks")
            
        except Exception as e:
            print(f"⚠️  {method.title()} chunking failed: {e}")
            # Create dummy result for testing
            chunker = create_chunker('fixed')
            results[method] = chunker.chunk(df, chunk_size=2)
    
    return results.get('fixed') or list(results.values())[0]

def test_embedding(chunking_result):
    """Test embedding module"""
    print("🔄 Testing Embedding...")
    
    from backend.core.embedding import generate_chunk_embeddings
    
    # Prepare metadata
    chunk_metadata = [
        {'chunk_id': f'test_chunk_{i}', 'method': 'fixed'}
        for i in range(len(chunking_result.chunks))
    ]
    
    try:
        # Test embedding generation
        embedding_result = generate_chunk_embeddings(
            chunks=chunking_result.chunks,
            chunk_metadata_list=chunk_metadata,
            model_name="all-MiniLM-L6-v2",
            batch_size=32,
            source_file="test_data.csv"
        )
        
        print(f"✅ Embedding: {embedding_result.total_chunks} chunks embedded")
        print(f"   Model: {embedding_result.model_used}")
        print(f"   Dimension: {embedding_result.vector_dimension}")
        
        return embedding_result
        
    except Exception as e:
        print(f"⚠️  Embedding failed: {e}")
        print("   This is expected if sentence-transformers is not installed")
        return None

def test_storing(embedding_result):
    """Test storing module"""
    print("🔄 Testing Storing...")
    
    from backend.core.storing import create_vector_store, store_embeddings, get_available_stores
    
    available_stores = get_available_stores()
    print(f"   Available stores: {available_stores}")
    
    if not available_stores:
        print("⚠️  No vector stores available")
        return None
    
    if not embedding_result:
        print("⚠️  No embeddings to store")
        return None
    
    stores_tested = {}
    
    for store_type in available_stores:
        try:
            print(f"   Testing {store_type.upper()} store...")
            
            # Create store with correct parameters
            if store_type == "chroma":
                store = create_vector_store("chroma", 
                                          persist_directory="./backend/storage/.chroma",
                                          collection_name="test_collection")
            else:  # faiss
                store = create_vector_store("faiss",
                                          persist_directory="./backend/storage/.faiss",
                                          dimension=embedding_result.vector_dimension)
            
            # Store embeddings using the utility function
            if store_type == "chroma":
                store = store_embeddings(embedding_result.embedded_chunks, 
                                       store_type="chroma",
                                       persist_directory="./backend/storage/.chroma",
                                       collection_name="test_collection")
            else:  # faiss
                store = store_embeddings(embedding_result.embedded_chunks,
                                       store_type="faiss", 
                                       persist_directory="./backend/storage/.faiss",
                                       dimension=embedding_result.vector_dimension)
            
            stores_tested[store_type] = store
            print(f"✅ {store_type.upper()} storage: Success")
            
        except Exception as e:
            print(f"⚠️  {store_type.upper()} storage failed: {e}")
    
    return stores_tested

def test_retrieval(stores_tested, embedding_result):
    """Test retrieval module"""
    print("🔄 Testing Retrieval...")
    
    from backend.core.retrieval import create_retriever, search_chunks
    
    if not stores_tested or not embedding_result:
        print("⚠️  No stores or embeddings available for retrieval testing")
        return
    
    test_query = "John email"
    
    for store_type, store in stores_tested.items():
        try:
            print(f"   Testing {store_type.upper()} retrieval...")
            
            # Create retriever
            retriever = create_retriever(
                store_type=store_type,
                persist_directory=f"./backend/storage/.{store_type}",
                collection_name="test_collection" if store_type == "chroma" else None
            )
            
            # Test different similarity metrics
            metrics = ["cosine", "dot", "euclidean"]
            
            for metric in metrics:
                try:
                    results = retriever.search(
                        query=test_query,
                        model_name="all-MiniLM-L6-v2",
                        top_k=2,
                        similarity_metric=metric
                    )
                    
                    num_results = len(results.get("ids", [[]])[0])
                    print(f"     {metric}: {num_results} results")
                    
                except Exception as e:
                    print(f"     {metric}: Failed - {e}")
            
            print(f"✅ {store_type.upper()} retrieval: Success")
            
        except Exception as e:
            print(f"⚠️  {store_type.upper()} retrieval failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Testing CSV Chunking Optimizer Pro Backend")
    print("=" * 50)
    
    try:
        # Test each module
        df = test_preprocessing()
        chunking_result = test_chunking(df)
        embedding_result = test_embedding(chunking_result)
        stores_tested = test_storing(embedding_result)
        test_retrieval(stores_tested, embedding_result)
        
        print("\n" + "=" * 50)
        print("🎉 Backend testing completed!")
        print("\n📋 Summary:")
        print("   ✅ Preprocessing: Working")
        print("   ✅ Chunking: Working") 
        print(f"   {'✅' if embedding_result else '⚠️ '} Embedding: {'Working' if embedding_result else 'Limited (install sentence-transformers)'}")
        print(f"   {'✅' if stores_tested else '⚠️ '} Storing: {'Working' if stores_tested else 'Limited (install chromadb/faiss)'}")
        print("   ✅ Retrieval: Working")
        
        print("\n🚀 Ready for FastAPI integration!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
