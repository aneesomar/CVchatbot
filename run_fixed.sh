#!/bin/bash

# Comprehensive fix script for chatbot
echo "🔧 Setting up clean environment for chatbot..."

# Export environment variables to fix issues
export ANONYMIZED_TELEMETRY=False
export CHROMA_TELEMETRY=False
export DO_NOT_TRACK=1
export TOKENIZERS_PARALLELISM=false
export CUDA_VISIBLE_DEVICES=""
export OMP_NUM_THREADS=1
export HF_HOME="$HOME/.cache/huggingface"
export TRANSFORMERS_CACHE="$HOME/.cache/huggingface/transformers"

# Suppress Python warnings
export PYTHONWARNINGS="ignore"

echo "✅ Environment variables configured!"

# Create cache directories if they don't exist
mkdir -p "$HOME/.cache/huggingface/transformers"

echo "🔍 Checking vector store..."
if [ -d "./vector_store" ] && [ "$(ls -A ./vector_store)" ]; then
    echo "✅ Vector store exists and has content"
else
    echo "🔄 Rebuilding vector store with CV data..."
    ./.venv/bin/python rebuild_vectorstore.py
fi

echo ""
echo "🚀 Starting Streamlit app..."
echo "Your chatbot will now use your actual CV data instead of fake information!"
echo ""

# Run streamlit with the virtual environment
./.venv/bin/streamlit run app.py
