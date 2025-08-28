#!/usr/bin/env python3
"""
Test script to verify chatbot retrieval is working with actual CV data
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

print("🔍 Testing chatbot with actual CV data...")

try:
    from document_processor import DocumentProcessor
    from chatbot_agent import PersonalChatbotAgent
    from suppress_chromadb import suppress_chromadb_output
    import config
    
    # Initialize document processor
    dp = DocumentProcessor()
    
    # Load the vector store
    print("📁 Loading vector store...")
    with suppress_chromadb_output():
        vector_store = dp.load_existing_vector_store()
    
    if not vector_store:
        print("❌ No vector store found. Run rebuild_vectorstore.py first.")
        sys.exit(1)
        
    # Check vector store content
    collection = vector_store._collection
    count = collection.count()
    print(f"✅ Vector store loaded with {count} documents")
    
    # Create retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    print("✅ Retriever created")
    
    # Test retrieval
    print("🔍 Testing document retrieval...")
    test_docs = retriever.get_relevant_documents("education university")
    print(f"✅ Retrieved {len(test_docs)} relevant documents")
    
    for i, doc in enumerate(test_docs[:2]):
        print(f"\nDocument {i+1}: {doc.page_content[:100]}...")
    
    # Initialize chatbot with retriever
    print("\n🤖 Initializing chatbot with retriever...")
    chatbot = PersonalChatbotAgent(vector_store_retriever=retriever)
    
    # Test a question
    print("\n❓ Testing chatbot with a question about education...")
    response = chatbot.ask("What is Anees's educational background?")
    
    print(f"\n🤖 Chatbot response:")
    print(f"Answer: {response['answer']}")
    print(f"Source documents: {len(response.get('source_documents', []))}")
    
    if response.get('source_documents'):
        print("\n📄 Source document previews:")
        for i, doc in enumerate(response['source_documents'][:2]):
            print(f"Source {i+1}: {doc.page_content[:100]}...")
    
    print("\n🎉 Chatbot test complete!")
    
except Exception as e:
    print(f"❌ Error during testing: {str(e)}")
    import traceback
    traceback.print_exc()
