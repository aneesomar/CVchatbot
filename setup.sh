#!/bin/bash
# Personal Chatbot Setup Script

echo "🤖 Setting up Personal AI Chatbot..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed. Please install it:"
    echo "   curl -fsSL https://ollama.ai/install.sh | sh"
    echo "   ollama pull llama3.2:1b"
else
    echo "✅ Ollama is installed"
    
    # Check if the model is pulled
    if ollama list | grep -q "llama3.2:1b"; then
        echo "✅ Model llama3.2:1b is available"
    else
        echo "📥 Pulling llama3.2:1b model..."
        ollama pull llama3.2:1b
    fi
fi

echo "🚀 Setup complete! Run the app with:"
echo "   source .venv/bin/activate && streamlit run app.py"
