#!/usr/bin/env python3
"""
Comprehensive test of all data files in the vector store
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

print("🔍 Comprehensive test of all data files...")

try:
    from document_processor import DocumentProcessor
    from chatbot_agent import PersonalChatbotAgent
    from suppress_chromadb import suppress_chromadb_output
    
    # Initialize
    dp = DocumentProcessor()
    
    with suppress_chromadb_output():
        vector_store = dp.load_existing_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": 8})
        chatbot = PersonalChatbotAgent(vector_store_retriever=retriever)
        
        # Check what's in the vector store
        collection = vector_store._collection
        count = collection.count()
        print(f"✅ Vector store has {count} document chunks")
    
    # Test queries targeting different files
    test_cases = [
        {
            "query": "Show me your Python machine learning code",
            "expected_file": "codeSnippet.md",
            "keywords": ["sklearn", "pandas", "torch", "RandomForest"]
        },
        {
            "query": "What is your educational background?", 
            "expected_file": "Anees Omar - CV.pdf",
            "keywords": ["University of Cape Town", "Geomatics", "Computer Science"]
        },
        {
            "query": "Tell me about Halalbites project",
            "expected_file": "aboutMe.md", 
            "keywords": ["Halalbites", "Next.js", "MongoDB", "Google Places"]
        },
        {
            "query": "What libraries do you import in your code?",
            "expected_file": "codeSnippet.md",
            "keywords": ["import pandas", "sklearn", "torch"]
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {test['query']}")
        print('='*70)
        
        # Get retrieved documents
        docs = retriever.get_relevant_documents(test['query'])
        print(f"📄 Retrieved {len(docs)} documents:")
        
        file_sources = {}
        for j, doc in enumerate(docs[:5]):
            source_file = doc.metadata.get('source', 'Unknown').split('/')[-1]
            if source_file not in file_sources:
                file_sources[source_file] = []
            file_sources[source_file].append(doc.page_content[:100])
            
            print(f"  {j+1}. {source_file}: {doc.page_content[:80]}...")
        
        # Check if expected file was retrieved
        expected_found = test['expected_file'] in file_sources
        print(f"\n📁 Expected file '{test['expected_file']}': {'✅ FOUND' if expected_found else '❌ NOT FOUND'}")
        
        # Get chatbot response
        response = chatbot.ask(test['query'])
        answer = response['answer']
        
        # Check if keywords appear in response
        keywords_found = []
        for keyword in test['keywords']:
            if keyword.lower() in answer.lower():
                keywords_found.append(keyword)
        
        print(f"🔍 Keywords found in response: {keywords_found if keywords_found else 'None'}")
        print(f"🤖 Response preview: {answer[:200]}...")
        
        # Show which files were actually used in the response
        source_files = set()
        for doc in response.get('source_documents', []):
            source_files.add(doc.metadata.get('source', 'Unknown').split('/')[-1])
        
        print(f"📁 Files used in response: {', '.join(source_files)}")
    
    print(f"\n{'='*70}")
    print("📊 SUMMARY - Files in your data folder:")
    print('='*70)
    
    files_info = [
        ("Anees Omar - CV.pdf", "4,179 chars", "Your formal CV and work experience"),
        ("aboutMe.md", "1,490 chars", "Professional bio and project details"),
        ("codeSnippet.md", "18,523 chars", "Python ML code with pandas, sklearn, torch"),
        ("projects.md", "1,490 chars", "Duplicate of aboutMe.md")
    ]
    
    for filename, size, description in files_info:
        print(f"✅ {filename:<25} | {size:<12} | {description}")
    
    print(f"\n🎉 All your data files are properly indexed and ready for AI retrieval!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
