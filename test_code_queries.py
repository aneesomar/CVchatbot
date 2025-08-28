#!/usr/bin/env python3
"""
Test code-specific queries to see if modelTraining.py is being used
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

try:
    import sys
    from unittest.mock import MagicMock
    sys.modules['posthog'] = MagicMock()
except:
    pass

print("🔍 Testing code-specific queries...")

try:
    from document_processor import DocumentProcessor
    from chatbot_agent import PersonalChatbotAgent
    from suppress_chromadb import suppress_chromadb_output
    
    # Initialize
    dp = DocumentProcessor()
    
    with suppress_chromadb_output():
        vector_store = dp.load_existing_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        chatbot = PersonalChatbotAgent(vector_store_retriever=retriever)
    
    # Test code-specific queries
    code_queries = [
        "Show me your Python code",
        "What machine learning libraries do you use?",
        "Do you have experience with scikit-learn?",
        "What is your experience with model training?",
        "Tell me about your data preprocessing techniques"
    ]
    
    for i, query in enumerate(code_queries, 1):
        print(f"\n{'='*50}")
        print(f"Query {i}: {query}")
        print('='*50)
        
        # Get relevant documents
        docs = retriever.get_relevant_documents(query)
        print(f"📄 Retrieved documents:")
        
        code_file_found = False
        for j, doc in enumerate(docs[:5]):
            source = doc.metadata.get('source', 'Unknown').split('/')[-1]
            if source == 'modelTraining.py':
                code_file_found = True
                print(f"  ✅ {source}: {doc.page_content[:80]}...")
            else:
                print(f"  📄 {source}: {doc.page_content[:80]}...")
        
        if code_file_found:
            print("  🎉 Code file WAS retrieved!")
        else:
            print("  ❌ Code file was NOT retrieved for this query")
    
    # Let's also search directly in the vector store for code content
    print(f"\n{'='*50}")
    print("Direct search for code-related content:")
    print('='*50)
    
    direct_search_terms = ["import pandas", "sklearn", "StandardScaler", "train_test_split"]
    
    for term in direct_search_terms:
        docs = retriever.get_relevant_documents(term)
        code_docs = [doc for doc in docs if 'modelTraining.py' in doc.metadata.get('source', '')]
        
        if code_docs:
            print(f"✅ Found '{term}' in modelTraining.py")
            print(f"   Content: {code_docs[0].page_content[:100]}...")
        else:
            print(f"❌ '{term}' not found in retrieved documents")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
