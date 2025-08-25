import streamlit as st
import os
from pathlib import Path
import tempfile

# Import our modules
from document_processor import DocumentProcessor
from chatbot_agent_free import FreePersonalChatbotAgent
import config_free as config

# Page configuration
st.set_page_config(
    page_title="Free Personal Chatbot",
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
        st.session_state.chatbot_agent = FreePersonalChatbotAgent()
    if "vector_store_ready" not in st.session_state:
        st.session_state.vector_store_ready = False

def check_ollama_status():
    """Check if Ollama is running and display status"""
    agent = FreePersonalChatbotAgent()
    if agent.is_ollama_available():
        st.success(f"✅ Ollama is running with model: {config.OLLAMA_MODEL}")
        return True
    else:
        st.error("❌ Ollama is not available. Please make sure Ollama is running.")
        st.info("Run: `ollama serve` in terminal to start Ollama")
        return False

def process_documents(uploaded_files):
    """Process uploaded documents and create vector store"""
    if not uploaded_files:
        return False
    
    with st.spinner("Processing documents..."):
        documents = []
        
        for uploaded_file in uploaded_files:
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                
                # Process based on file type
                if uploaded_file.name.endswith('.pdf'):
                    docs = st.session_state.doc_processor.load_pdf(tmp_file_path)
                elif uploaded_file.name.endswith('.docx'):
                    docs = st.session_state.doc_processor.load_docx(tmp_file_path)
                elif uploaded_file.name.endswith('.txt'):
                    docs = st.session_state.doc_processor.load_text_file(tmp_file_path)
                else:
                    st.warning(f"Unsupported file type: {uploaded_file.name}")
                    continue
                
                documents.extend(docs)
                
                # Clean up temp file
                os.unlink(tmp_file_path)
                
                st.success(f"✅ Processed {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                continue
        
        if documents:
            # Create vector store (this will use local embeddings, no API calls)
            try:
                vector_store = st.session_state.doc_processor.create_vector_store_free(documents)
                retriever = vector_store.as_retriever(search_kwargs={"k": 3})
                
                # Update chatbot agent with new retriever
                st.session_state.chatbot_agent = FreePersonalChatbotAgent(vector_store_retriever=retriever)
                st.session_state.vector_store_ready = True
                
                st.success(f"✅ Successfully processed {len(documents)} documents!")
                return True
                
            except Exception as e:
                st.error(f"Error creating vector store: {str(e)}")
                return False
        
        return False

def main():
    st.title("🤖 Free Personal Chatbot")
    st.markdown("**Powered by Ollama (100% Free & Local)**")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.header("📄 Document Management")
        
        # Check Ollama status
        ollama_available = check_ollama_status()
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload your documents",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            help="Upload PDF, DOCX, or TXT files containing information about you"
        )
        
        if st.button("Process Documents") and ollama_available:
            if uploaded_files:
                success = process_documents(uploaded_files)
                if success:
                    st.rerun()
            else:
                st.warning("Please upload some documents first")
        
        # Status
        st.subheader("📊 Status")
        if st.session_state.vector_store_ready:
            st.success("✅ Documents ready for questions")
        else:
            st.info("📤 Upload documents to enable Q&A")
        
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
    if prompt := st.chat_input("Ask me anything about the uploaded documents..."):
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
    
    # Sample questions (when no documents are loaded)
    if not st.session_state.vector_store_ready:
        st.subheader("💡 Get Started")
        st.info("Upload your personal documents (CV, projects, notes) in the sidebar to enable document-based Q&A!")
        
        st.subheader("🤖 Or chat directly:")
        sample_questions = [
            "Tell me about yourself",
            "What can you help me with?",
            "How do you work?"
        ]
        
        cols = st.columns(len(sample_questions))
        for i, question in enumerate(sample_questions):
            if cols[i].button(question, key=f"sample_{i}"):
                st.session_state.messages.append({"role": "user", "content": question})
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        answer = st.session_state.chatbot_agent.chat_direct(question)
                        st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()

if __name__ == "__main__":
    main()
