import streamlit as st
import os
from pathlib import Path

# Apply ChromaDB telemetry patch first
try:
    import sys
    from unittest.mock import MagicMock
    sys.modules['posthog'] = MagicMock()
except:
    pass

# Suppress warnings
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Import our modules
from document_processor import DocumentProcessor
from chatbot_agent import PersonalChatbotAgent
import config

# Page configuration
st.set_page_config(
    page_title="Anees's Personal AI Assistant (FREE)",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "doc_processor" not in st.session_state:
        st.session_state.doc_processor = DocumentProcessor()
    if "chatbot_agent" not in st.session_state:
        st.session_state.chatbot_agent = PersonalChatbotAgent()
    if "vector_store_ready" not in st.session_state:
        st.session_state.vector_store_ready = False
        # Try to automatically load documents from data folder on startup
        load_documents_from_data_folder()

def check_ollama_status():
    """Check if Ollama is running and display status"""
    agent = PersonalChatbotAgent()
    if agent.is_ollama_available():
        st.success(f"✅ Ollama is running with model: {config.OLLAMA_MODEL}")
        return True
    else:
        st.error("❌ Ollama is not available. Please make sure Ollama is running.")
        st.info("Run: `ollama serve` in terminal to start Ollama")
        return False

def load_documents_from_data_folder():
    """Automatically load and process documents from the data folder"""
    try:
        # Check if data folder exists
        if not os.path.exists(config.DATA_FOLDER):
            st.info(f"📁 Creating data folder: {config.DATA_FOLDER}")
            os.makedirs(config.DATA_FOLDER, exist_ok=True)
            st.info("Please add your documents to the data folder and click 'Refresh Documents'")
            return False
        
        # Try to load existing vector store first
        try:
            with st.spinner("Loading existing documents..."):
                from utils.suppress_chromadb import suppress_chromadb_output
                
                with suppress_chromadb_output():
                    vector_store = st.session_state.doc_processor.load_existing_vector_store()
                
                if vector_store:
                    # Check if vector store has content
                    collection = vector_store._collection
                    count = collection.count()
                    
                    if count > 0:
                        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
                        st.session_state.chatbot_agent = PersonalChatbotAgent(vector_store_retriever=retriever)
                        st.session_state.vector_store_ready = True
                        st.success(f"✅ Loaded existing vector store with {count} document chunks")
                        return True
                    else:
                        st.info("Existing vector store is empty, processing documents...")
        except Exception as e:
            st.info(f"Could not load existing vector store ({str(e)}), processing documents...")
        
        # Process documents from data folder
        documents = st.session_state.doc_processor.process_documents(config.DATA_FOLDER)
        
        if not documents:
            st.info(f"📁 No documents found in {config.DATA_FOLDER}. Add some documents and click 'Refresh Documents'")
            return False
        
        # Create vector store
        with st.spinner(f"Processing {len(documents)} documents from data folder..."):
            from utils.suppress_chromadb import suppress_chromadb_output
            
            with suppress_chromadb_output():
                vector_store = st.session_state.doc_processor.create_vector_store(documents)
            
            if vector_store:
                retriever = vector_store.as_retriever(search_kwargs={"k": 3})
                st.session_state.chatbot_agent = PersonalChatbotAgent(vector_store_retriever=retriever)
                st.session_state.vector_store_ready = True
                st.success(f"✅ Successfully processed {len(documents)} documents!")
                return True
            else:
                st.error("Failed to create vector store")
                return False
                
    except Exception as e:
        st.error(f"Error loading documents: {str(e)}")
        return False

def main():
    st.title("🤖 Anees's Personal AI Assistant (FREE)")
    st.markdown("**Powered by Ollama (100% Free & Local) • Trained on Data Folder**")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.header("� Document Management")
        
        # Check Ollama status
        ollama_available = check_ollama_status()
        
        # Data folder info
        data_folder_exists = os.path.exists(config.DATA_FOLDER)
        if data_folder_exists:
            file_count = sum([len(files) for r, d, files in os.walk(config.DATA_FOLDER)])
            st.info(f"📊 Data folder: {file_count} files found")
        else:
            st.warning(f"📁 Data folder not found: {config.DATA_FOLDER}")
        
        # Refresh documents button
        if st.button("🔄 Refresh Documents", help="Reprocess documents from data folder") and ollama_available:
            success = load_documents_from_data_folder()
            if success:
                st.rerun()
        
        # Instructions
        st.subheader("📋 Instructions")
        st.markdown(f"""
        1. Add your documents to: `{config.DATA_FOLDER}`
        2. Supported formats: PDF, DOCX, TXT, MD, PY, JS, HTML, CSS, JSON
        3. Click **Refresh Documents** to process new files
        """)
        
        # Status
        st.subheader("📊 Status")
        if st.session_state.vector_store_ready:
            st.success("✅ Documents ready for questions")
        else:
            st.info("📤 Add documents to data folder and refresh")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            if hasattr(st.session_state, "chatbot_agent"):
                st.session_state.chatbot_agent.clear_memory()
            st.rerun()
        
        # Model info
        st.subheader("🔧 Model Info")
        st.info(f"**Model**: {config.OLLAMA_MODEL}")
        st.info("**Cost**: 100% Free")
        st.info("**Privacy**: Runs locally")
    
    # Main chat interface
    if not ollama_available:
        st.warning("⚠️ Ollama is not running. Please start Ollama to use the chatbot.")
        st.code("ollama serve", language="bash")
        return
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Anees..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if st.session_state.vector_store_ready:
                    response = st.session_state.chatbot_agent.ask(prompt)
                    answer = response["answer"]
                else:
                    # Use direct chat without documents
                    answer = st.session_state.chatbot_agent.chat_direct(prompt)
                
                st.markdown(answer)
                
                # Show source documents if available
                if st.session_state.vector_store_ready and "source_documents" in response:
                    source_docs = response["source_documents"]
                    if source_docs:
                        with st.expander("📚 Sources"):
                            for i, doc in enumerate(source_docs):
                                st.write(f"**Source {i+1}:**")
                                st.write(doc.page_content[:200] + "...")
        
        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # Sample questions
    if not st.session_state.vector_store_ready:
        st.subheader("💡 Get Started")
        st.info(f"Add your personal documents to the `{config.DATA_FOLDER}` folder and click 'Refresh Documents' in the sidebar to enable document-based Q&A!")
        
        st.subheader("🤖 Or chat directly:")
        sample_questions = [
            "Tell me about yourself",
            "What can you help me with?",
            "How do you work?"
        ]
    else:
        st.subheader("💡 Sample Questions About Anees")
        sample_questions = [
            "What is Anees's educational background?",
            "What programming languages does Anees know?",
            "Tell me about Anees's work experience",
            "What projects has Anees worked on?",
            "What are Anees's technical skills?",
            "What is Anees's contact information?"
        ]
    
    cols = st.columns(min(3, len(sample_questions)))  # Max 3 columns
    for i, question in enumerate(sample_questions):
        col_idx = i % len(cols)
        if cols[col_idx].button(question, key=f"sample_{i}"):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    if st.session_state.vector_store_ready:
                        response = st.session_state.chatbot_agent.ask(question)
                        answer = response["answer"]
                    else:
                        answer = st.session_state.chatbot_agent.chat_direct(question)
                    st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

if __name__ == "__main__":
    main()
