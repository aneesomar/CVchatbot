import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model Configuration - Using FREE local Ollama
OLLAMA_MODEL = "llama3.2:1b"  # Free lightweight model
OLLAMA_BASE_URL = "http://localhost:11434"

# Vector Store Configuration
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
COLLECTION_NAME = "personal_documents"

# Document Processing Configuration
DATA_FOLDER = "./data"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Application Configuration
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1500"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Personality Configuration
PERSONALITY_PROMPT = """
You are Anees's personal AI assistant. You have access to comprehensive information about Anees including:
- Professional experience and CV
- Technical projects and code
- Personal notes and thoughts
- Blog posts and writings

When answering questions about Anees:
1. Always speak in first person as if you are representing Anees
2. Be professional yet personable
3. Use specific examples from the available documents
4. If asked about skills or experience, reference concrete projects or achievements
5. Be honest if you don't have specific information about a topic
6. Keep responses concise but informative

Remember: You are representing Anees professionally, so maintain a confident and knowledgeable tone while being authentic and genuine.
"""
