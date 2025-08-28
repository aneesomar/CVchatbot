#!/usr/bin/env python3
"""
Test specific queries about the new data files
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

print("🔍 Testing chatbot with queries about new data files...")

try:
    from document_processor import DocumentProcessor
    from chatbot_agent import PersonalChatbotAgent
    from suppress_chromadb import suppress_chromadb_output
    import config
    
    # Initialize
    dp = DocumentProcessor()
    
    with suppress_chromadb_output():
        vector_store = dp.load_existing_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        chatbot = PersonalChatbotAgent(vector_store_retriever=retriever)
    
    # Test queries about different aspects
    test_queries = [
        "Tell me about your programming skills and technical experience",
        "What projects have you worked on?", 
        "What are your interests and background?",
        "Show me some of your code or technical work",
        "What machine learning or data science experience do you have?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {query}")
        print('='*60)
        
        # Get relevant documents first
        docs = retriever.get_relevant_documents(query)
        print(f"📄 Retrieved {len(docs)} relevant documents:")
        
        for j, doc in enumerate(docs[:3]):
            source = doc.metadata.get('source', 'Unknown').split('/')[-1]
            print(f"  {j+1}. {source}: {doc.page_content[:100]}...")
        
        # Get chatbot response
        response = chatbot.ask(query)
        print(f"\n🤖 Response:")
        print(f"{response['answer'][:300]}...")
        
        # Check what files were referenced
        sources = set()
        for doc in response.get('source_documents', []):
            source_file = doc.metadata.get('source', 'Unknown').split('/')[-1]
            sources.add(source_file)
        
        print(f"\n📁 Sources used: {', '.join(sources)}")
    
    print(f"\n🎉 All tests completed!")
    
except Exception as e:
    print(f"❌ Error during testing: {str(e)}")
    import traceback
    traceback.print_exc()
