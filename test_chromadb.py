#!/usr/bin/env python3
"""Test ChromaDB compatibility with LangChain 0.0.325"""

import os
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Load environment variables
load_dotenv()

def test_chromadb_compatibility():
    print("Testing ChromaDB compatibility with LangChain 0.0.325...")
    
    try:
        # Initialize OpenAI embeddings
        embeddings = OpenAIEmbeddings()
        print("✅ OpenAI embeddings initialized successfully")
        
        # Test creating a vector store with sample documents
        sample_texts = [
            "I am an experienced software engineer with expertise in Python and machine learning.",
            "My projects include building chatbots and web applications using modern frameworks.",
            "I have worked with technologies like LangChain, Streamlit, and OpenAI APIs."
        ]
        
        # Create ChromaDB vector store
        vector_store = Chroma.from_texts(
            texts=sample_texts,
            embedding=embeddings,
            persist_directory="./test_chroma_db"
        )
        print("✅ ChromaDB vector store created successfully")
        
        # Test similarity search
        results = vector_store.similarity_search("software engineer", k=2)
        print(f"✅ Similarity search returned {len(results)} results")
        for i, doc in enumerate(results):
            print(f"  {i+1}. {doc.page_content}")
        
        print("\n🎉 ChromaDB compatibility test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ ChromaDB compatibility test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chromadb_compatibility()
    exit(0 if success else 1)
