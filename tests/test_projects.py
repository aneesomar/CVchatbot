#!/usr/bin/env python3
"""
Test if project information is accessible by the AI
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

print("🔍 Testing if your projects are loaded and accessible...")

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
    
    print(f"✅ Vector store loaded with {vector_store._collection.count()} document chunks")
    
    # Test project-specific queries
    project_queries = [
        "Tell me about your Halalbites project",
        "What is your landslide susceptibility modeling thesis about?",
        "Tell me about PlantGen project",
        "What machine learning projects have you worked on?",
        "What web development projects have you built?",
        "Describe your final year thesis project"
    ]
    
    for i, query in enumerate(project_queries, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {query}")
        print('='*60)
        
        # Get retrieved documents
        docs = retriever.get_relevant_documents(query)
        
        # Check if projects.md is retrieved
        projects_found = False
        for doc in docs[:5]:
            source_file = doc.metadata.get('source', 'Unknown').split('/')[-1]
            print(f"📄 {source_file}: {doc.page_content[:80]}...")
            if source_file == 'projects.md':
                projects_found = True
        
        if projects_found:
            print("✅ projects.md WAS retrieved for this query")
        else:
            print("⚠️  projects.md was NOT retrieved for this query")
        
        # Get AI response
        response = chatbot.ask(query)
        answer = response['answer']
        
        # Check for specific project keywords
        project_keywords = {
            'Halalbites': ['halalbites', 'next.js', 'mongodb', 'mapbox', 'restaurant'],
            'Landslide': ['landslide', 'susceptibility', 'chiapas', 'mexico', 'ann', 'neural'],
            'PlantGen': ['plantgen', 'simulation', 'plant growth', 'viability', 'sampler']
        }
        
        found_projects = []
        for project, keywords in project_keywords.items():
            if any(keyword.lower() in answer.lower() for keyword in keywords):
                found_projects.append(project)
        
        print(f"🎯 Projects mentioned in response: {found_projects if found_projects else 'None detected'}")
        print(f"🤖 Response preview: {answer[:150]}...")
        
        # Show source files used
        source_files = set()
        for doc in response.get('source_documents', []):
            source_files.add(doc.metadata.get('source', 'Unknown').split('/')[-1])
        print(f"📁 Source files used: {', '.join(source_files)}")
    
    print(f"\n{'='*60}")
    print("📊 PROJECTS SUMMARY")
    print('='*60)
    
    # Test direct retrieval of project content
    project_terms = ["Halalbites", "landslide susceptibility", "PlantGen"]
    
    for term in project_terms:
        docs = retriever.get_relevant_documents(term)
        project_docs = [doc for doc in docs if 'projects.md' in doc.metadata.get('source', '')]
        
        if project_docs:
            print(f"✅ Found '{term}' in projects.md: {project_docs[0].page_content[:100]}...")
        else:
            print(f"❌ '{term}' not found in retrieved project documents")
    
    print("\n🎉 Project accessibility test complete!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
