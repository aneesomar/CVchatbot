#!/usr/bin/env python3
"""
Context manager to suppress ChromaDB telemetry errors
"""
import sys
import os
from contextlib import contextmanager
from io import StringIO

@contextmanager
def suppress_chromadb_output():
    """Context manager to suppress ChromaDB telemetry errors"""
    # Save the original stderr
    original_stderr = sys.stderr
    
    try:
        # Redirect stderr to capture telemetry errors
        captured_output = StringIO()
        sys.stderr = captured_output
        
        yield
        
    finally:
        # Get what was captured
        captured = captured_output.getvalue()
        
        # Restore original stderr
        sys.stderr = original_stderr
        
        # Only print non-telemetry errors
        lines = captured.split('\n')
        for line in lines:
            if line and not any(x in line.lower() for x in [
                'failed to send telemetry',
                'capture() takes 1 positional argument',
                'clientstartevent',
                'clientcreatecollectionevent', 
                'collectionqueryevent'
            ]):
                print(line, file=sys.stderr)

def safe_chromadb_import():
    """Safely import chromadb with suppressed telemetry"""
    with suppress_chromadb_output():
        import chromadb
        return chromadb

if __name__ == "__main__":
    print("🔇 ChromaDB output suppression utility loaded!")
    
    # Test the suppression
    print("Testing ChromaDB with suppressed telemetry...")
    with suppress_chromadb_output():
        import chromadb
        client = chromadb.Client()
        collection = client.create_collection("test_suppress")
        print("✅ ChromaDB operations completed silently!")
