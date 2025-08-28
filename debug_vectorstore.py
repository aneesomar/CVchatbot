#!/usr/bin/env python3
"""
Debug script to check what's actually in the vector store
"""
import os
import sys

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

print("🔍 Debugging vector store content...")

try:
    from document_processor import DocumentProcessor
    from suppress_chromadb import suppress_chromadb_output
    import config
    
    # Initialize document processor
    dp = DocumentProcessor()
    
    # Check if vector store exists and has content
    print("📁 Checking vector store...")
    
    with suppress_chromadb_output():
        vector_store = dp.load_existing_vector_store()
        
        if vector_store:
            # Get the collection
            collection = vector_store._collection
            print(f"✅ Vector store loaded. Collection name: {collection.name}")
            
            # Check how many documents are in the collection
            count = collection.count()
            print(f"📊 Document count in vector store: {count}")
            
            if count > 0:
                # Get a few sample documents to see what's stored
                results = collection.peek(limit=3)
                print("\n📄 Sample documents in vector store:")
                
                if results and 'documents' in results:
                    for i, doc in enumerate(results['documents'][:3]):
                        print(f"\n--- Document {i+1} ---")
                        print(f"Content preview: {doc[:200]}...")
                        if 'metadatas' in results and i < len(results['metadatas']):
                            print(f"Metadata: {results['metadatas'][i]}")
                else:
                    print("❌ No documents found in results")
            else:
                print("❌ Vector store is empty!")
        else:
            print("❌ Could not load vector store")
    
    # Also check if the PDF can be read
    print("\n📄 Checking PDF processing...")
    pdf_path = "/home/anees/chatBot/data/Anees Omar - CV.pdf"
    if os.path.exists(pdf_path):
        print(f"✅ PDF file exists: {pdf_path}")
        
        # Try to load the PDF
        documents = dp.load_pdf(pdf_path)
        if documents:
            print(f"✅ PDF loaded successfully. Content length: {len(documents[0].page_content)} characters")
            print(f"📄 PDF content preview:\n{documents[0].page_content[:300]}...")
        else:
            print("❌ Failed to load PDF content")
    else:
        print(f"❌ PDF file not found: {pdf_path}")
        
except Exception as e:
    print(f"❌ Error during debugging: {str(e)}")
    import traceback
    traceback.print_exc()
