#!/usr/bin/env python3
"""
Test script to verify the environment fixes work
"""
import os
import sys

# Set environment variables first
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False" 
os.environ["DO_NOT_TRACK"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["OMP_NUM_THREADS"] = "1"

print("🧪 Testing environment fixes...")

try:
    # Test sentence transformers import
    print("📦 Testing sentence-transformers...")
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
    print("✅ Sentence transformers working!")
    
    # Test ChromaDB import
    print("📦 Testing ChromaDB...")
    import chromadb
    print("✅ ChromaDB import successful!")
    
    # Test creating a simple embedding
    print("📦 Testing embeddings...")
    test_text = "This is a test sentence."
    embedding = model.encode([test_text])
    print(f"✅ Embedding created! Shape: {embedding.shape}")
    
    # Test basic ChromaDB functionality
    print("📦 Testing ChromaDB functionality...")
    client = chromadb.Client()
    collection = client.create_collection("test_collection")
    print("✅ ChromaDB collection created successfully!")
    
    print("\n🎉 All tests passed! Environment is properly configured.")
    
except Exception as e:
    print(f"❌ Error during testing: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    sys.exit(1)
