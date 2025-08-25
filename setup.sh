#!/bin/bash

# Setup script for Personal Chatbot
echo "🤖 Setting up your Personal Chatbot..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OpenAI API key!"
else
    echo "✅ .env file already exists"
fi

# Create data folder if it doesn't exist
if [ ! -d "data" ]; then
    echo "📁 Creating data folder..."
    mkdir -p data
    mkdir -p data/code_snippets
    echo "✅ Data folder created"
else
    echo "✅ Data folder already exists"
fi

# Check if vector store exists
if [ -d "vector_store" ]; then
    echo "🗄️  Vector store found"
else
    echo "🗄️  Vector store will be created on first run"
fi

echo ""
echo "🚀 Setup complete! Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Add your personal documents to the data/ folder"
echo "3. Run: streamlit run app.py"
echo ""
echo "📚 Document types supported:"
echo "   - PDF files (CV, documents)"
echo "   - Word documents (.docx)"
echo "   - Text files (.txt, .md)"
echo "   - Code files (.py, .js, .html, .css, .json)"
echo ""
echo "💡 Sample documents have been created in data/ - replace them with your own!"
