# 🤖 Personal Context-Aware Chatbot - Quick Start Guide

## Overview
Your personal AI assistant that knows everything about you! This chatbot uses your CV, projects, code snippets, and personal notes to answer questions about your background, skills, and experience.

## 🚀 Quick Start (5 minutes)

### 1. Set up your OpenAI API key
```bash
# Edit the .env file
nano .env

# Replace this line:
OPENAI_API_KEY=your_openai_api_key_here

# With your actual API key:
OPENAI_API_KEY=sk-your-actual-openai-key
```

### 2. Add your personal documents
```bash
# Your documents go in the data/ folder:
data/
├── cv.pdf                    # Your resume/CV
├── about_me.md              # Professional summary (template provided)
├── projects.md              # Your projects (template provided)  
├── notes.md                 # Personal thoughts (template provided)
└── code_snippets/
    ├── data_processing.py   # Code examples (samples provided)
    └── error_handling.js
```

### 3. Run the application
```bash
# Test everything is set up correctly
./test.sh

# Launch the chatbot
./run.sh

# Or manually:
streamlit run app.py
```

## 📋 What to Put in Each File

### `data/about_me.md` - Your Professional Profile
- Technical skills and expertise levels
- Programming languages you know
- Frameworks and tools you use
- Work experience and achievements
- Education and certifications
- Personal interests that relate to your work

### `data/projects.md` - Your Project Portfolio  
- Detailed project descriptions
- Technologies used
- Challenges you solved
- Quantifiable achievements
- Code repositories (if public)
- Impact and lessons learned

### `data/notes.md` - Your Engineering Philosophy
- Your approach to problem-solving
- What motivates you as an engineer
- Career goals and aspirations
- Favorite technologies and why
- Work style and collaboration preferences
- Values and principles

### `data/code_snippets/` - Code Examples
- Functions you frequently use
- Problem-solving patterns
- Code that represents your style
- Comments explaining your approach
- Examples from different languages/frameworks

## 🎯 Sample Questions You Can Ask

**About Skills:**
- "What programming languages do you know best?"
- "What's your experience with Python/JavaScript/etc?"
- "What frameworks have you worked with?"

**About Projects:**  
- "What projects are you most proud of?"
- "Tell me about a challenging project you worked on"
- "What technologies did you use in [specific project]?"

**About Experience:**
- "What kind of engineer are you?"
- "What's your problem-solving approach?"
- "What are your career goals?"

**Technical Questions:**
- "Show me some code examples"
- "How do you handle errors in your code?"
- "What's your development philosophy?"

## 🔧 Customization

### Personality Configuration
Edit `config.py` to modify how the chatbot responds:
- Adjust temperature for creativity vs. consistency
- Modify the personality prompt
- Change chunk sizes for document processing

### Document Types Supported
- **PDF files**: CVs, documents
- **Word documents**: .docx files
- **Text files**: .txt, .md (Markdown)
- **Code files**: .py, .js, .html, .css, .json, etc.

### Vector Store
The app uses ChromaDB to store document embeddings:
- Located in `vector_store/` folder
- Automatically created when you first process documents
- Persists between sessions

## 🐛 Troubleshooting

### "No OpenAI API Key" Error
- Check your `.env` file has the correct key
- Make sure there's no extra spaces or quotes
- Verify the key starts with `sk-`

### "No documents found" Warning
- Add documents to the `data/` folder
- Click "Refresh Documents" in the sidebar
- Check the file formats are supported

### Chatbot gives generic responses
- Add more specific information to your documents
- Include concrete examples and details
- The more context you provide, the better the responses

### Performance is slow
- Reduce `CHUNK_SIZE` in config.py for faster processing
- Use fewer documents initially to test
- Check your internet connection for OpenAI API calls

## 📁 Project Structure
```
chatBot/
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document loading and vector storage
├── chatbot_agent.py      # LangChain conversational agent
├── config.py             # Configuration and personality settings
├── data/                 # Your personal documents
│   ├── about_me.md
│   ├── projects.md
│   ├── notes.md
│   └── code_snippets/
├── vector_store/         # ChromaDB storage (auto-created)
├── .env                  # Environment variables (your API key)
├── requirements.txt      # Python dependencies
├── setup.sh             # Setup script
├── run.sh               # Launch script
└── test.sh              # Test script
```

## 💡 Tips for Best Results

1. **Be Specific**: Include concrete examples, numbers, and details
2. **Use Your Voice**: Write in your natural style - the bot will learn it
3. **Include Context**: Explain why you made certain technical decisions
4. **Update Regularly**: Add new projects and experiences as they happen
5. **Test Often**: Try different questions to see how well the bot knows you

## 🔒 Privacy & Security

- All processing happens locally except for OpenAI API calls
- Your documents are stored locally in the vector database
- Only relevant chunks are sent to OpenAI for generating responses
- Consider using OpenAI's data usage policies for sensitive information

---

**Ready to create your personal AI assistant? Start by editing your `.env` file and adding your documents to the `data/` folder!**
