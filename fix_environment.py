#!/usr/bin/env python3
"""
Script to fix environment and compatibility issues
"""
import os
import sys
import subprocess

def set_environment_variables():
    """Set environment variables to prevent telemetry and torch issues"""
    env_vars = {
        # Disable ChromaDB telemetry
        "ANONYMIZED_TELEMETRY": "False",
        "CHROMA_TELEMETRY": "False", 
        "DO_NOT_TRACK": "1",
        
        # Fix tokenizer parallelism warning
        "TOKENIZERS_PARALLELISM": "false",
        
        # Force CPU usage for PyTorch to avoid CUDA issues
        "CUDA_VISIBLE_DEVICES": "",
        "OMP_NUM_THREADS": "1",
        
        # Set HuggingFace cache to avoid permission issues
        "HF_HOME": os.path.expanduser("~/.cache/huggingface"),
        "TRANSFORMERS_CACHE": os.path.expanduser("~/.cache/huggingface/transformers"),
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"Set {key}={value}")

def main():
    """Main function to fix environment"""
    print("🔧 Fixing environment and compatibility issues...")
    
    # Set environment variables
    set_environment_variables()
    
    print("✅ Environment variables configured!")
    print("\n📝 To make these permanent, add to your ~/.bashrc:")
    print("export ANONYMIZED_TELEMETRY=False")
    print("export CHROMA_TELEMETRY=False")
    print("export DO_NOT_TRACK=1")
    print("export TOKENIZERS_PARALLELISM=false")
    print("export CUDA_VISIBLE_DEVICES=''")
    print("export OMP_NUM_THREADS=1")

if __name__ == "__main__":
    main()
