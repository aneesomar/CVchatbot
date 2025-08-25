#!/bin/bash

# Launch script for Personal Chatbot

echo "🤖 Starting Personal Chatbot..."

# Activate virtual environment if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Run the Streamlit app
echo "🚀 Launching Streamlit app..."
streamlit run app.py
