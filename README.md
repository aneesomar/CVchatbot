# Personal Chatbot - OpenAI-Powered Context-Aware Assistant

This chatbot is designed to answer questions about me using my personal data including CV, projects, notes, code snippets, and blog posts. It uses OpenAI's powerful GPT models for intelligent responses.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aneesomar/CVchatbot.git
   cd CVchatbot
   ```

2. **Set up virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenAI API**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. **Access the chatbot**:
   Open your browser and go to http://localhost:8501

### Streamlit Cloud Deployment
This project is optimized for Streamlit Cloud deployment. Simply:
1. Push your code to GitHub
2. Connect your repo to Streamlit Cloud
3. Add your `OPENAI_API_KEY` in the Streamlit Cloud secrets
4. Deploy!

## Features

- 🤖 **OpenAI-Powered** - Uses GPT-3.5-turbo or GPT-4 for intelligent responses
- 🧠 **Context-aware responses** based on personal data
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
