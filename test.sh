#!/bin/bash

# Quick test script for the Personal Chatbot

echo "🧪 Testing Personal Chatbot Setup..."

# Check if .env exists and has API key
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please run ./setup.sh first"
    exit 1
fi

# Check if OPENAI_API_KEY is set
if grep -q "your_openai_api_key_here" .env; then
    echo "❌ Please set your real OpenAI API key in .env file"
    echo "   Edit .env and replace 'your_openai_api_key_here' with your actual key"
    exit 1
fi

echo "✅ Environment file looks good"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Check dependencies
echo "🔍 Checking dependencies..."
python -c "import streamlit, langchain, openai; print('✅ All packages installed')" 2>/dev/null || {
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
}

# Check data folder
if [ -d "data" ] && [ "$(ls -A data)" ]; then
    echo "✅ Data folder contains files"
    echo "📁 Files in data folder:"
    find data -type f | head -5
else
    echo "⚠️  Data folder is empty or doesn't exist"
    echo "   Add your personal documents to the data/ folder before running the app"
fi

echo ""
echo "🚀 Ready to launch! Run: streamlit run app.py"
echo "💡 Or use: ./run.sh (if it exists)"
