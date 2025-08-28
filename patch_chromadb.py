#!/usr/bin/env python3
"""
Patch ChromaDB to completely suppress telemetry errors
"""
import sys
import warnings
from unittest.mock import MagicMock

# Suppress all warnings before importing anything
warnings.filterwarnings('ignore')

# Mock the problematic telemetry components
sys.modules['posthog'] = MagicMock()

def patch_chromadb():
    """Patch ChromaDB to prevent telemetry issues"""
    try:
        import chromadb.telemetry.posthog as posthog_module
        
        # Replace the problematic capture method
        def mock_capture(*args, **kwargs):
            pass
        
        if hasattr(posthog_module, 'Posthog'):
            posthog_module.Posthog.capture = mock_capture
            
    except ImportError:
        pass
    
    try:
        # Also patch at the chromadb level
        import chromadb
        if hasattr(chromadb, 'telemetry'):
            chromadb.telemetry = MagicMock()
    except ImportError:
        pass

# Apply the patch
patch_chromadb()

print("🔇 ChromaDB telemetry patched - no more telemetry errors!")
