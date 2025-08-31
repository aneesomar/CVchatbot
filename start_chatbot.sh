#!/bin/bash

# ChatBot Startup Script
echo "🚀 Starting ChatBot with Ngrok..."

# Activate virtual environment
source venv/bin/activate

# Set environment variables to suppress warnings
export TOKENIZERS_PARALLELISM=false
export TORCH_LOGS="+dynamo"
export TORCH_DISABLE_WARN=1

# Start Streamlit with better configuration
echo "📱 Starting Streamlit app..."
streamlit run app.py \
    --server.port=8501 \
    --server.headless=true \
    --server.address=0.0.0.0 \
    --server.enableCORS=true \
    --server.enableXsrfProtection=false \
    --logger.level=error

echo "✅ ChatBot stopped."
