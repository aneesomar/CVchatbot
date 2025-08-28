#!/usr/bin/env python3
"""
Simple check of data folder content without loading models
"""
import os

print("📁 Current data folder contents:")
print("="*50)

data_folder = "/home/anees/chatBot/data"

for filename in os.listdir(data_folder):
    file_path = os.path.join(data_folder, filename)
    
    if os.path.isfile(file_path):
        # Get file size
        size = os.path.getsize(file_path)
        
        print(f"\n📄 {filename}")
        print(f"   Size: {size:,} bytes")
        
        # Try to read first few lines to see content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(200)
                print(f"   Preview: {content[:150]}...")
        except:
            print(f"   (Binary file or encoding issue)")

print("\n" + "="*50)

# Check if vector store exists
vector_store_path = "/home/anees/chatBot/vector_store"
if os.path.exists(vector_store_path):
    print("✅ Vector store directory exists")
    
    # Count files in vector store
    total_files = 0
    for root, dirs, files in os.walk(vector_store_path):
        total_files += len(files)
    
    print(f"📊 Vector store contains {total_files} files")
else:
    print("❌ No vector store found")

print("\n🎯 Project keywords to look for in your files:")
project_keywords = [
    "Halalbites", "landslide susceptibility", "PlantGen", 
    "Next.js", "MongoDB", "Chiapas", "Mexico", "ANN", 
    "neural network", "QGIS plugin", "simulation"
]

print("Keywords:", ", ".join(project_keywords))
