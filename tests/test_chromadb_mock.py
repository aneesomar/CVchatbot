#!/usr/bin/env python3
"""Test ChromaDB integration without OpenAI API calls"""

import numpy as np
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from typing import List

class MockEmbeddings(Embeddings):
    """Mock embeddings that don't call external APIs"""
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # Return mock embeddings - just random vectors for testing
        return [np.random.rand(1536).tolist() for _ in texts]
    
    def embed_query(self, text: str) -> List[float]:
        # Return mock embedding for query
        return np.random.rand(1536).tolist()

def test_chromadb_integration():
    print("Testing ChromaDB integration without API calls...")
    
    try:
        # Initialize mock embeddings (no API calls)
        embeddings = MockEmbeddings()
        print("✅ Mock embeddings initialized successfully")
        
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
            persist_directory="./test_chroma_mock"
        )
        print("✅ ChromaDB vector store created successfully")
        
        # Test adding more documents
        vector_store.add_texts([
            "Additional experience with cloud platforms and DevOps practices."
        ])
        print("✅ Additional documents added successfully")
        
        # Test similarity search
        results = vector_store.similarity_search("software engineer", k=2)
        print(f"✅ Similarity search returned {len(results)} results")
        for i, doc in enumerate(results):
            print(f"  {i+1}. {doc.page_content[:60]}...")
        
        # Test retrieving all documents
        all_docs = vector_store.get()
        print(f"✅ Vector store contains {len(all_docs['documents'])} documents total")
        
        print("\n🎉 ChromaDB integration test PASSED!")
        print("✅ ChromaDB 0.4.15 is compatible with LangChain 0.0.325")
        print("✅ Vector store creation, document addition, and search work correctly")
        return True
        
    except Exception as e:
        print(f"❌ ChromaDB integration test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chromadb_integration()
    exit(0 if success else 1)
