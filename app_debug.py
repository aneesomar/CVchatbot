import streamlit as st
import os
from document_processor import DocumentProcessor
from chatbot_agent import PersonalChatbotAgent, SAMPLE_QUESTIONS
import config

def check_environment():
    """Check if the environment is properly configured."""
    issues = []
    
    # Check OpenAI API key
    if not config.OPENAI_API_KEY:
        issues.append("❌ OPENAI_API_KEY not found in environment variables")
    elif config.OPENAI_API_KEY == "your_openai_api_key_here":
        issues.append("❌ Please set your real OpenAI API key in .env file")
    elif not config.OPENAI_API_KEY.startswith("sk-"):
        issues.append("⚠️ OpenAI API key should start with 'sk-'")
    else:
        issues.append("✅ OpenAI API key configured")
    
    # Check data folder
    if os.path.exists(config.DATA_FOLDER):
        file_count = sum([len(files) for r, d, files in os.walk(config.DATA_FOLDER)])
        if file_count > 0:
            issues.append(f"✅ Data folder contains {file_count} files")
        else:
            issues.append("⚠️ Data folder is empty")
    else:
        issues.append("❌ Data folder does not exist")
    
    return issues

def main():
    st.set_page_config(
        page_title="Anees's Personal AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 Anees's Personal AI Assistant")
    st.markdown("*Ask me anything about Anees - his skills, projects, experience, and more!*")
    
    # Environment check
    with st.sidebar:
        st.header("🔧 System Status")
        issues = check_environment()
        for issue in issues:
            if issue.startswith("✅"):
                st.success(issue)
            elif issue.startswith("⚠️"):
                st.warning(issue)
            else:
                st.error(issue)
        
        st.divider()
        st.header("📁 Document Management")
        
        if st.button("🔄 Refresh Documents", help="Process documents from the data folder"):
            try:
                with st.spinner("Processing documents..."):
                    processor = DocumentProcessor()
                    vector_store = processor.update_documents()
                    if vector_store:
                        st.session_state['vector_store'] = vector_store
                        st.success("Documents processed successfully!")
                    else:
                        st.error("Failed to process documents")
            except Exception as e:
                st.error(f"Error processing documents: {str(e)}")
                st.code(str(e))
    
    # Check if we can proceed
    critical_issues = [issue for issue in check_environment() if issue.startswith("❌")]
    if critical_issues:
        st.error("Please fix the critical issues shown in the sidebar before using the chatbot.")
        st.info("💡 Quick fixes:")
        st.markdown("""
        1. **Set OpenAI API Key**: Edit `.env` file and add your key
        2. **Add Documents**: Put your files in the `data/` folder
        3. **Click Refresh Documents** in the sidebar
        """)
        return
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    # Try to load vector store
    if 'vector_store' not in st.session_state:
        try:
            processor = DocumentProcessor()
            vector_store = processor.load_existing_vector_store()
            if vector_store:
                st.session_state['vector_store'] = vector_store
                st.sidebar.success("Vector store loaded")
            else:
                st.sidebar.warning("No vector store found. Click 'Refresh Documents'")
        except Exception as e:
            st.sidebar.error(f"Error loading vector store: {str(e)}")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state and 'vector_store' in st.session_state:
        try:
            retriever = st.session_state['vector_store'].as_retriever(search_kwargs={"k": 4})
            st.session_state['chatbot'] = PersonalChatbotAgent(retriever)
            st.sidebar.success("Chatbot initialized")
        except Exception as e:
            st.sidebar.error(f"Error initializing chatbot: {str(e)}")
            st.code(str(e))
    
    # Main interface
    if 'chatbot' in st.session_state:
        # Display messages
        for message in st.session_state['messages']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.write(f"**{i}. {source['filename']}** ({source['type']})")
                            st.text(source['content_preview'])
                            if i < len(message["sources"]):
                                st.divider()
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about Anees..."):
            # Add user message
            st.session_state['messages'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get assistant response
            with st.chat_message("assistant"):
                try:
                    with st.spinner("Thinking..."):
                        response = st.session_state['chatbot'].ask(prompt)
                    
                    st.markdown(response['answer'])
                    
                    if response['sources']:
                        with st.expander("📚 Sources"):
                            for i, source in enumerate(response['sources'], 1):
                                st.write(f"**{i}. {source['filename']}** ({source['type']})")
                                st.text(source['content_preview'])
                                if i < len(response['sources']):
                                    st.divider()
                    
                    # Add to session
                    st.session_state['messages'].append({
                        "role": "assistant", 
                        "content": response['answer'],
                        "sources": response['sources']
                    })
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.code(str(e))
                    st.session_state['messages'].append({
                        "role": "assistant", 
                        "content": error_msg,
                        "sources": []
                    })
        
        # Sample questions in sidebar
        with st.sidebar:
            st.divider()
            st.header("💡 Sample Questions")
            for i, question in enumerate(SAMPLE_QUESTIONS[:3]):
                if st.button(question, key=f"sample_{i}"):
                    st.session_state['current_question'] = question
                    st.rerun()
            
            with st.expander("More questions..."):
                for i, question in enumerate(SAMPLE_QUESTIONS[3:8], 3):
                    if st.button(question, key=f"sample_{i}"):
                        st.session_state['current_question'] = question
                        st.rerun()
        
        # Handle sample question selection
        if 'current_question' in st.session_state:
            question = st.session_state['current_question']
            del st.session_state['current_question']
            
            # Add to messages and process
            st.session_state['messages'].append({"role": "user", "content": question})
            
            try:
                response = st.session_state['chatbot'].ask(question)
                st.session_state['messages'].append({
                    "role": "assistant", 
                    "content": response['answer'],
                    "sources": response['sources']
                })
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state['messages'].append({
                    "role": "assistant", 
                    "content": error_msg,
                    "sources": []
                })
            
            st.rerun()
        
        # Clear conversation
        if st.sidebar.button("🗑️ Clear Conversation") and st.session_state['messages']:
            st.session_state['messages'] = []
            if 'chatbot' in st.session_state:
                st.session_state['chatbot'].clear_memory()
            st.rerun()
    
    else:
        st.info("Please set up the system using the sidebar controls to start chatting.")
        
        # Show sample questions for preview
        st.subheader("💡 Example Questions You Can Ask")
        cols = st.columns(2)
        with cols[0]:
            for question in SAMPLE_QUESTIONS[:5]:
                st.markdown(f"• {question}")
        with cols[1]:
            for question in SAMPLE_QUESTIONS[5:10]:
                st.markdown(f"• {question}")

if __name__ == "__main__":
    main()
