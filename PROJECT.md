# Personal AI Chatbot

A FREE, privacy-focused personal AI assistant that learns from your documents and data.

## 📁 Project Structure

```
chatBot/
├── 🚀 Core Application
│   ├── app.py                    # Main Streamlit application
│   ├── chatbot_agent.py         # AI chatbot logic and Ollama integration
│   ├── document_processor.py    # Document processing and vector store
│   ├── config.py               # Configuration and personality modes
│   └── requirements.txt        # Python dependencies
│
├── 📊 Your Data
│   └── data/                   # Personal documents (CV, projects, notes)
│       ├── aboutMe.md
│       ├── Anees Omar - CV.pdf
│       ├── codeSnippet.md
│       └── projects.md
│
├── 🧪 Tests
│   └── tests/                  # Application tests
│       ├── test_all_data.py
│       ├── test_app_simulation.py
│       ├── test_chatbot_retrieval.py
│       ├── test_code_queries.py
│       ├── test_environment.py
│       ├── test_new_data.py
│       └── test_projects.py
│
├── 📚 Documentation
│   └── docs/
│       ├── README.md           # Detailed documentation
│       └── QUICKSTART.md       # Quick setup guide
│
├── 🔧 Utilities
│   └── utils/
│       └── suppress_chromadb.py # ChromaDB output suppression
│
├── 💾 Generated Data
│   └── vector_store/           # ChromaDB vector database (auto-generated)
│
└── 📋 Configuration
    ├── README.md               # This file
    ├── setup.sh               # Easy setup script
    ├── .env.example           # Environment variables template
    └── .gitignore             # Git ignore rules
```

## 🚀 Quick Start

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Start the application:**
   ```bash
   source .venv/bin/activate
   streamlit run app.py
   ```

3. **Add your documents** to the `data/` folder and refresh in the app!

## ✨ Features

- 🆓 **100% FREE** - Uses local Ollama LLM (no API costs)
- 🔒 **Privacy-First** - All data stays on your machine
- 🧠 **Context-Aware** - Learns from your personal documents
- 💬 **Conversational** - Natural chat interface with memory
- 🎭 **Multiple Personalities** - Professional, casual, technical modes
- 📚 **Auto-Learning** - Automatically processes documents from `data/` folder
