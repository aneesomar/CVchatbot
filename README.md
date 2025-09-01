# Personal Chatbot - OpenAI-Powered Context-Aware Assistant

This chatbot is designed to answer questions about me using my personal data including CV, projects, notes, code snippets, and blog posts. It uses OpenAI's powerful GPT models for intelligent responses and FAISS for efficient document retrieval.

## ✨ Features

- 🤖 **OpenAI GPT Integration** - Powered by ChatGPT for intelligent responses
- 📚 **Document Processing** - Supports PDF, DOCX, TXT, MD, PY, JS, HTML, CSS, JSON
- 🔍 **FAISS Vector Search** - Fast and efficient document retrieval (no SQLite dependencies)
- 🎭 **Multiple Personality Modes** - Interview, storytelling, technical expert, and more
- 🌐 **Streamlit Cloud Ready** - Optimized for easy deployment
- 💬 **Chat Memory** - Maintains conversation context
- 🔒 **Secure** - API keys handled safely through environment variables or Streamlit secrets

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

This project is optimized for Streamlit Cloud deployment:

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy CVchatbot to Streamlit Cloud"
git push origin main
```

#### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Choose your repository and branch (main)
5. Set the main file path to `app.py`

#### Step 3: Configure Secrets
1. In your Streamlit Cloud dashboard, click "Manage app"
2. Go to the "Secrets" tab
3. Add your OpenAI API key:
   ```toml
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```
4. Save and redeploy

#### Step 4: Upload Your Data
After deployment, add your personal documents to the `data/` folder and use the "Refresh Documents" button in the app.

### Environment Variables
The app looks for the OpenAI API key in this order:
1. Environment variable `OPENAI_API_KEY`
2. Streamlit Cloud secrets
3. Local `.env` file

### 🔧 Local Development with Streamlit Secrets
For local testing with Streamlit secrets:
1. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
2. Add your API key to the file
3. Run the app normally

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
