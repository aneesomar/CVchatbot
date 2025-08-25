# Personal Chatbot - Context-Aware Assistant

This chatbot is designed to answer questions about me using my personal data including CV, projects, notes, code snippets, and blog posts.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

3. Add your personal documents to the `data/` folder:
   - `cv.pdf` - Your CV/Resume
   - `projects.md` - Project descriptions
   - `notes.md` - Personal notes
   - `code_snippets/` - Code examples
   - `blog_posts/` - Blog posts or articles

4. Run the application:
```bash
streamlit run app.py
```

## Features

- Context-aware responses based on personal data
- Document ingestion and vector storage
- Conversational interface
- Personality-aware responses
- Technical and personal question handling

## Project Structure

```
chatBot/
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document loading and processing
├── chatbot_agent.py      # LangChain agent and memory
├── config.py             # Configuration settings
├── data/                 # Personal documents
│   ├── cv.pdf
│   ├── projects.md
│   ├── notes.md
│   └── code_snippets/
├── vector_store/         # ChromaDB storage
└── requirements.txt
```
