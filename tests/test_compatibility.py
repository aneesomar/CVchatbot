#!/usr/bin/env python3
"""Test script to verify all imports and basic functionality."""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all required imports."""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        print("✅ LangChain OpenAI imports successful")
    except ImportError as e:
        print(f"❌ LangChain OpenAI import failed: {e}")
        return False
    
    try:
        from langchain_community.vectorstores import Chroma
        print("✅ ChromaDB import successful")
    except ImportError as e:
        print(f"❌ ChromaDB import failed: {e}")
        return False
    
    try:
        import config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    return True

def test_document_processor():
    """Test DocumentProcessor class."""
    print("\nTesting DocumentProcessor...")
    
    try:
        from document_processor import DocumentProcessor
        print("✅ DocumentProcessor import successful")
        
        # Only test initialization if we have an API key
        if hasattr(__import__('config'), 'OPENAI_API_KEY') and __import__('config').OPENAI_API_KEY and __import__('config').OPENAI_API_KEY != 'your_openai_api_key_here':
            processor = DocumentProcessor()
            print("✅ DocumentProcessor initialization successful")
        else:
            print("⚠️  Skipping DocumentProcessor initialization (no API key set)")
            
    except Exception as e:
        print(f"❌ DocumentProcessor failed: {e}")
        return False
    
    return True

def test_chatbot_agent():
    """Test PersonalChatbotAgent class."""
    print("\nTesting PersonalChatbotAgent...")
    
    try:
        from chatbot_agent import PersonalChatbotAgent
        print("✅ PersonalChatbotAgent import successful")
        
    except Exception as e:
        print(f"❌ PersonalChatbotAgent failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🧪 Running compatibility tests...\n")
    
    all_passed = True
    
    if not test_imports():
        all_passed = False
    
    if not test_document_processor():
        all_passed = False
    
    if not test_chatbot_agent():
        all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All tests passed! The application should work correctly.")
        print("💡 Next steps:")
        print("   1. Set your OpenAI API key in .env")
        print("   2. Add documents to data/ folder")
        print("   3. Run: streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
