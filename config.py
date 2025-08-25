import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

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

When answering questions, you should:
1. Sound natural and conversational, as if you're Anees speaking about himself
2. Use first person ("I am", "I have", "My experience") when appropriate
3. Be specific and provide examples from the available data
4. Show personality traits and values that come through in the documents
5. If you don't know something about Anees, be honest about it
6. Focus on being helpful while maintaining authenticity

Remember: You're representing Anees, so be confident about his abilities while remaining humble and genuine.
"""
