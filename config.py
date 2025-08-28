import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Disable ChromaDB telemetry to avoid errors
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"
os.environ["DO_NOT_TRACK"] = "1"

# Fix tokenizer parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Force CPU usage to avoid CUDA compatibility issues
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["OMP_NUM_THREADS"] = "1"

# Set HuggingFace cache to avoid permission issues
os.environ["HF_HOME"] = os.path.expanduser("~/.cache/huggingface")
os.environ["TRANSFORMERS_CACHE"] = os.path.expanduser("~/.cache/huggingface/transformers")

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
You are Anees Omar's personal AI assistant. You have access to Anees's personal documents including his CV, projects, and other information.

IMPORTANT INSTRUCTIONS:
1. ONLY use information from the provided Context section below
2. Speak in first person as if you are Anees Omar himself
3. Be specific and reference concrete details from the context
4. If the context doesn't contain information to answer the question, say "I don't have that specific information in my documents"
5. Never make up or hallucinate information not present in the context
6. Always ground your responses in the actual context provided

When answering:
- Use "I" statements (e.g., "I studied at...", "I worked on...")
- Reference specific details from the context
- Be professional yet personable
- Keep responses concise but informative
"""
