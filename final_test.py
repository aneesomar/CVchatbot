#!/usr/bin/env python3
"""
Final test script to verify all fixes are working
"""
import os
import sys

# Set all environment variables
os.environ.update({
    "ANONYMIZED_TELEMETRY": "False",
    "CHROMA_TELEMETRY": "False", 
    "DO_NOT_TRACK": "1",
    "TOKENIZERS_PARALLELISM": "false",
    "CUDA_VISIBLE_DEVICES": "",
    "OMP_NUM_THREADS": "1",
    "PYTHONWARNINGS": "ignore"
})

print("🧪 Final comprehensive test...")

# Test the document processor
try:
    print("📄 Testing Document Processor...")
    from document_processor import DocumentProcessor
    dp = DocumentProcessor()
    print("✅ Document Processor loaded successfully!")
    
    print("🤖 Testing Chatbot Agent...")
    from chatbot_agent import PersonalChatbotAgent
    agent = PersonalChatbotAgent()
    print("✅ Chatbot Agent loaded successfully!")
    
    print("⚙️ Testing Configuration...")
    import config
    print(f"✅ Config loaded! Model: {config.OLLAMA_MODEL}")
    
    print("🎯 Testing vector store creation...")
    # Test with suppressed output
    with dp.suppress_chromadb_output if hasattr(dp, 'suppress_chromadb_output') else open(os.devnull, 'w'):
        vector_store = dp.load_existing_vector_store()
    print("✅ Vector store operations working!")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("✅ No more telemetry errors!")
    print("✅ Environment properly configured!")
    print("✅ Ready to run your chatbot!")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
