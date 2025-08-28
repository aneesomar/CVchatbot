#!/usr/bin/env python3
"""
Quick test to simulate the app initialization and verify chatbot responses
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

print("🧪 Simulating app initialization and testing chatbot responses...")

class MockSessionState:
    def __init__(self):
        self.messages = []
        self.doc_processor = None
        self.chatbot_agent = None
        self.vector_store_ready = False

try:
    from document_processor import DocumentProcessor
    from chatbot_agent import PersonalChatbotAgent
    from suppress_chromadb import suppress_chromadb_output
    import config
    
    # Simulate session state initialization
    print("🔄 Initializing session state...")
    session_state = MockSessionState()
    session_state.doc_processor = DocumentProcessor()
    session_state.chatbot_agent = PersonalChatbotAgent()
    session_state.vector_store_ready = False
    
    # Simulate load_documents_from_data_folder function
    print("📁 Loading documents from data folder...")
    
    # Load existing vector store
    with suppress_chromadb_output():
        vector_store = session_state.doc_processor.load_existing_vector_store()
    
    if vector_store:
        collection = vector_store._collection
        count = collection.count()
        
        if count > 0:
            retriever = vector_store.as_retriever(search_kwargs={"k": 3})
            session_state.chatbot_agent = PersonalChatbotAgent(vector_store_retriever=retriever)
            session_state.vector_store_ready = True
            print(f"✅ Vector store loaded with {count} document chunks")
        else:
            print("❌ Vector store is empty")
    
    # Test questions
    test_questions = [
        "What is your educational background?",
        "What technical skills do you have?",
        "Tell me about your work experience?"
    ]
    
    print(f"\n🤖 Testing chatbot (vector_store_ready: {session_state.vector_store_ready})...")
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n--- Test Question {i}: {question} ---")
        
        if session_state.vector_store_ready:
            response = session_state.chatbot_agent.ask(question)
            answer = response["answer"]
            source_count = len(response.get("source_documents", []))
            print(f"✅ Using retrieval (sources: {source_count})")
        else:
            answer = session_state.chatbot_agent.chat_direct(question)
            print("❌ Using direct chat (no retrieval)")
        
        # Show first 200 characters of answer
        print(f"Answer: {answer[:200]}...")
        
        # Check if it mentions real details from CV
        real_details = ["University of Cape Town", "Geomatics", "Computer Science", "BSc", "anees", "ANEES OMAR"]
        found_real = any(detail.lower() in answer.lower() for detail in real_details)
        fake_details = ["Stanford", "Google", "research assistant", "freelance consultant"]
        found_fake = any(detail.lower() in answer.lower() for detail in fake_details)
        
        if found_real and not found_fake:
            print("✅ Response contains real CV information")
        elif found_fake:
            print("❌ Response contains fake/hallucinated information")
        else:
            print("⚠️ Response doesn't contain clear CV details")
    
    print("\n🎉 Test complete!")
    
except Exception as e:
    print(f"❌ Error during testing: {str(e)}")
    import traceback
    traceback.print_exc()
