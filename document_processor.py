import os
import streamlit as st
from typing import List, Dict
import PyPDF2
import docx
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
import config

class LocalEmbeddings(Embeddings):
    """Free local embeddings using sentence-transformers (CPU only)"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Force CPU usage to avoid CUDA compatibility issues
        self.model = SentenceTransformer(model_name, device='cpu')
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        embedding = self.model.encode([text], convert_to_tensor=False)
        return embedding[0].tolist()

class DocumentProcessor:
    def __init__(self):
        # Always use free local embeddings
        self.embeddings = LocalEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        
    def load_pdf(self, file_path: str) -> List[Document]:
        """Extract text from PDF file."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return [Document(page_content=text, metadata={"source": file_path, "type": "pdf"})]
        except Exception as e:
            st.error(f"Error reading PDF {file_path}: {str(e)}")
            return []
    
    def load_docx(self, file_path: str) -> List[Document]:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return [Document(page_content=text, metadata={"source": file_path, "type": "docx"})]
        except Exception as e:
            st.error(f"Error reading DOCX {file_path}: {str(e)}")
            return []
    
    def load_text_file(self, file_path: str) -> List[Document]:
        """Load text from various text files."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                return [Document(page_content=text, metadata={"source": file_path, "type": "text"})]
        except Exception as e:
            st.error(f"Error reading text file {file_path}: {str(e)}")
            return []
        except Exception as e:
            st.error(f"Error reading text file {file_path}: {str(e)}")
            return ""
    
    def process_documents(self, data_folder: str) -> List[Document]:
        """Process all documents in the data folder."""
        documents = []
        
        if not os.path.exists(data_folder):
            st.warning(f"Data folder '{data_folder}' not found. Creating it...")
            os.makedirs(data_folder, exist_ok=True)
            return documents
        
        # Walk through all files in the data folder
        for root, dirs, files in os.walk(data_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                text_content = ""
                metadata = {"source": file_path, "filename": file}
                
                # Process different file types
                if file_ext == '.pdf':
                    text_content = self.load_pdf(file_path)
                    metadata["type"] = "PDF"
                elif file_ext == '.docx':
                    text_content = self.load_docx(file_path)
                    metadata["type"] = "Word Document"
                elif file_ext in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json']:
                    text_content = self.load_text_file(file_path)
                    metadata["type"] = "Text File"
                
                if text_content.strip():
                    # Create document object
                    doc = Document(page_content=text_content, metadata=metadata)
                    documents.append(doc)
        
        return documents
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create and populate vector store with documents using free local embeddings."""
        if not documents:
            st.warning("No documents found to process!")
            return None
        
        # Split documents into chunks
        split_documents = self.text_splitter.split_documents(documents)
        
        st.info(f"Processing {len(split_documents)} document chunks with free local embeddings...")
        
        # Create vector store with local embeddings
        vector_store = Chroma.from_documents(
            documents=split_documents,
            embedding=self.embeddings,
            collection_name=config.COLLECTION_NAME,
            persist_directory=config.VECTOR_STORE_PATH
        )
        
        vector_store.persist()
        return vector_store
    
    def load_existing_vector_store(self) -> Chroma:
        """Load existing vector store if it exists."""
        try:
            vector_store = Chroma(
                collection_name=config.COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=config.VECTOR_STORE_PATH
            )
            return vector_store
        except Exception as e:
            st.error(f"Error loading vector store: {str(e)}")
            return None
    
    def update_documents(self) -> Chroma:
        """Update the vector store with new documents."""
        documents = self.process_documents(config.DATA_FOLDER)
        if documents:
            return self.create_vector_store(documents)
        return self.load_existing_vector_store()
