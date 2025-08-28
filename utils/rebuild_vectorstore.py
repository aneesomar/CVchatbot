#!/usr/bin/env python3
"""
Script to rebuild the vector store with actual CV data
"""
import os
import sys
import shutil

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variables
os.environ.update({
    "ANONYMIZED_TELEMETRY": "False",
    "CHROMA_TELEMETRY": "False", 
    "DO_NOT_TRACK": "1",
    "TOKENIZERS_PARALLELISM": "false",
    "CUDA_VISIBLE_DEVICES": "",
    "OMP_NUM_THREADS": "1",
    "PYTHONWARNINGS": "ignore"
})

# Apply ChromaDB patches
try:
    import sys
    from unittest.mock import MagicMock
    sys.modules['posthog'] = MagicMock()
except:
    pass

print("🔄 Rebuilding vector store with actual CV data...")

try:
    from document_processor import DocumentProcessor
    from suppress_chromadb import suppress_chromadb_output
    import config
    
    # Initialize document processor
    dp = DocumentProcessor()
    
    # Delete existing vector store to start fresh
    if os.path.exists(config.VECTOR_STORE_PATH):
        print(f"🗑️ Removing existing vector store: {config.VECTOR_STORE_PATH}")
        shutil.rmtree(config.VECTOR_STORE_PATH)
    
    # Process documents from the data folder
    print("📁 Processing documents from data folder...")
    documents = dp.process_documents(config.DATA_FOLDER)
    
    if documents:
        print(f"✅ Found {len(documents)} documents to process")
        
        # Show preview of what we're storing
        for i, doc in enumerate(documents):
            print(f"\n--- Document {i+1}: {doc.metadata.get('source', 'Unknown')} ---")
            print(f"Type: {doc.metadata.get('type', 'Unknown')}")
            print(f"Content length: {len(doc.page_content)} characters")
            print(f"Content preview: {doc.page_content[:200]}...")
        
        # Create the vector store
        print("\n🔄 Creating vector store...")
        with suppress_chromadb_output():
            vector_store = dp.create_vector_store(documents)
        
        if vector_store:
            print("✅ Vector store created successfully!")
            
            # Verify the content
            collection = vector_store._collection
            count = collection.count()
            print(f"📊 Final document count: {count}")
            
            # Test a sample query
            print("\n🔍 Testing sample query...")
            results = vector_store.similarity_search("education university", k=2)
            if results:
                print("✅ Query successful! Sample results:")
                for i, result in enumerate(results[:2]):
                    print(f"\nResult {i+1}: {result.page_content[:150]}...")
            else:
                print("❌ Query returned no results")
                
        else:
            print("❌ Failed to create vector store")
    else:
        print("❌ No documents found to process")
        
    print("\n🎉 Vector store rebuild complete!")
    
except Exception as e:
    print(f"❌ Error during rebuild: {str(e)}")
    import traceback
    traceback.print_exc()
