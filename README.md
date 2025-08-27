# Personal Chatbot - FREE Context-Aware Assistant

This chatbot is designed to answer questions about me using my personal data including CV, projects, notes, code snippets, and blog posts. It uses **completely FREE** local models (Ollama) and embeddings - no API costs!

## Setup

1. **Install Ollama** (Free local AI):
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the required model
ollama pull llama3.2:1b
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Add your personal documents** to the `data/` folder:
   - `cv.pdf` - Your CV/Resume
   - `projects.md` - Project descriptions
   - `notes.md` - Personal notes
   - `code_snippets/` - Code examples
   - `blog_posts/` - Blog posts or articles

4. **Run the application**:
```bash
streamlit run app.py
```

## Features

- 🆓 **Completely FREE** - Uses local Ollama model and sentence-transformers
- 🧠 Context-aware responses based on personal data
- 📚 Document ingestion and vector storage (ChromaDB)
- 💬 Conversational interface with memory
- 🎭 Personality-aware responses
- 💻 Technical and personal question handling
- 🔒 Privacy-first - all data stays on your machine

## Project Structure

```
chatBot/
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document loading and processing (free embeddings)
├── chatbot_agent.py      # Ollama-based agent and memory
├── config.py             # Configuration settings
├── data/                 # Personal documents
│   ├── cv.pdf
│   ├── projects.md
│   ├── notes.md
│   └── code_snippets/
├── vector_store/         # ChromaDB storage
└── requirements.txt      # No OpenAI dependencies!
```
