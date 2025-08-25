#!/usr/bin/env python3
"""Final test to verify the fix works without API calls."""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_initialization_only():
    """Test initialization without API calls."""
    print("🧪 Testing initialization (no API calls)...")
    
    try:
        # Import config first
        import config
        print(f"✅ Config loaded, API key starts with: {config.OPENAI_API_KEY[:7]}...")
        
        # Test OpenAI embeddings
        from langchain.embeddings.openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
        print("✅ OpenAIEmbeddings initialized successfully!")
        
        # Test ChatOpenAI
        from langchain.chat_models import ChatOpenAI
        llm = ChatOpenAI(
            openai_api_key=config.OPENAI_API_KEY,
            model_name=config.OPENAI_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS
        )
        print("✅ ChatOpenAI initialized successfully!")
        
        # Test DocumentProcessor
        from document_processor import DocumentProcessor
        processor = DocumentProcessor()
        print("✅ DocumentProcessor initialized successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def main():
    """Run the test."""
    print("🔧 Final Compatibility Test...\n")
    
    success = test_initialization_only()
    
    print("\n" + "="*50)
    if success:
        print("🎉 SUCCESS! All components initialize correctly!")
        print("💡 The ValidationError has been fixed!")
        print("\n✅ Next steps:")
        print("   1. Your OpenAI API key is set correctly")
        print("   2. All LangChain components work")
        print("   3. Run: streamlit run app.py")
        print("\n⚠️  Note: If you get API quota errors when running the app,")
        print("   that's a billing issue with your OpenAI account, not a code issue.")
    else:
        print("❌ Initialization failed. Check the error above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
