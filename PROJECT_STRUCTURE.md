# Personal AI Chatbot - Clean Project Structure

## 📁 Project Organization

```
chatBot/
├── 📄 Core Application Files
│   ├── app.py                    # Main Streamlit application
│   ├── chatbot_agent.py         # ChatBot logic and AI interaction
│   ├── document_processor.py    # Document processing and vector store
│   ├── config.py               # Configuration and environment setup
│   └── requirements.txt        # Python dependencies
│
├── 📂 data/                    # Your personal data files
│   ├── Anees Omar - CV.pdf     # Your CV/resume
│   ├── aboutMe.md             # Professional bio
│   ├── projects.md            # Project descriptions  
│   └── codeSnippet.md         # Code examples
│
├── 📂 docs/                    # Documentation
│   ├── README.md              # Main project documentation
│   ├── CHATBOT_FIXED.md       # Fix documentation
│   ├── ENVIRONMENT_FIXES.md   # Environment issue solutions
│   ├── FIXES.md               # General fixes
│   └── QUICKSTART.md          # Quick start guide
│
├── 📂 tests/                   # Test scripts and utilities
│   ├── test_*.py              # Various test scripts
│   ├── check_data_simple.py   # Simple data verification
│   ├── debug_vectorstore.py   # Vector store debugging
│   └── test_chroma_mock/      # Test data
│
├── 📂 utils/                   # Utility scripts
│   ├── rebuild_vectorstore.py # Rebuild vector database
│   ├── suppress_chromadb.py   # ChromaDB output suppression
│   ├── fix_environment.py     # Environment fixes
│   └── patch_chromadb.py      # ChromaDB patches
│
├── 📂 vector_store/            # Vector database (auto-generated)
├── 📂 __pycache__/            # Python cache (auto-generated)
├── 📂 .venv/                  # Virtual environment
│
├── 🚀 Run Scripts
│   ├── run_fixed.sh           # Main run script (USE THIS!)
│   ├── run.sh                 # Original run script
│   ├── setup.sh               # Environment setup
│   └── test.sh                # Test runner
│
└── ⚙️ Configuration
    ├── .env                    # Environment variables (if exists)
    ├── .env.example           # Environment template
    ├── .gitignore             # Git ignore rules
    └── .git/                  # Git repository
```

## 🚀 How to Use

### Quick Start
```bash
./run_fixed.sh
```

### Manual Setup
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set up environment**: `./setup.sh`
3. **Add your data**: Put files in `data/` folder
4. **Run the app**: `./run_fixed.sh`

## 📊 What's Included

- ✅ **Your CV Data**: PDF automatically processed
- ✅ **Project Details**: All your projects from projects.md
- ✅ **Code Examples**: Your Python ML code from codeSnippet.md  
- ✅ **Professional Bio**: About me information
- ✅ **Clean Environment**: No telemetry errors or warnings
- ✅ **Vector Search**: Fast semantic search through your data

## 🛠️ Utilities

- **`utils/rebuild_vectorstore.py`**: Refresh the vector database with new data
- **`tests/debug_vectorstore.py`**: Check what's in your vector database
- **`utils/suppress_chromadb.py`**: Hide ChromaDB noise/errors

## 📝 Add New Data

1. Add files to `data/` folder (PDF, MD, TXT, etc.)
2. Run: `python utils/rebuild_vectorstore.py`
3. Restart the app: `./run_fixed.sh`

Your chatbot will automatically use the new information!

---
*Organized and cleaned project structure for better maintainability*
