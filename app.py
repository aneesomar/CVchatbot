import streamlit as st
import os
from document_processor import DocumentProcessor
from chatbot_agent import PersonalChatbotAgent, SAMPLE_QUESTIONS
import config

def main():
    st.set_page_config(
        page_title="Anees's Personal AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 Anees's Personal AI Assistant")
    st.markdown("*Ask me anything about Anees - his skills, projects, experience, and more!*")
    
    # Sidebar for configuration and document management
    with st.sidebar:
        st.header("📁 Document Management")
        
        # Check if OpenAI API key is set
        if not config.OPENAI_API_KEY:
            st.error("🔑 Please set your OpenAI API key in the .env file")
            st.code("OPENAI_API_KEY=your_api_key_here")
            st.stop()
        
        if config.OPENAI_API_KEY == "your_openai_api_key_here":
            st.error("🔑 Please set your real OpenAI API key in the .env file")
            st.code("OPENAI_API_KEY=sk-your-actual-key-here")
            st.stop()
        
        # Document processing section
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
                if "api_key" in str(e).lower():
                    st.info("💡 This might be an API key issue. Check your .env file.")
        
        # Show data folder info
        data_folder_exists = os.path.exists(config.DATA_FOLDER)
        if data_folder_exists:
            file_count = sum([len(files) for r, d, files in os.walk(config.DATA_FOLDER)])
            st.info(f"📊 Data folder: {file_count} files found")
        else:
            st.warning("📁 Data folder not found. Create 'data/' and add your documents.")
        
        # Sample questions
        st.header("💡 Sample Questions")
        st.markdown("Click on any question to ask:")
        
        for question in SAMPLE_QUESTIONS[:5]:  # Show first 5 questions
            if st.button(question, key=f"sample_{question[:20]}"):
                st.session_state['current_question'] = question
        
        # Show more questions in an expander
        with st.expander("More sample questions..."):
            for question in SAMPLE_QUESTIONS[5:]:
                if st.button(question, key=f"sample_more_{question[:20]}"):
                    st.session_state['current_question'] = question
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []
    
    if 'vector_store' not in st.session_state:
        # Try to load existing vector store
        try:
            processor = DocumentProcessor()
            vector_store = processor.load_existing_vector_store()
            if vector_store:
                st.session_state['vector_store'] = vector_store
            else:
                st.warning("⚠️ No documents found. Please add documents to the 'data/' folder and click 'Refresh Documents'.")
        except Exception as e:
            st.error(f"Error loading vector store: {str(e)}")
            if "api_key" in str(e).lower():
                st.info("💡 This might be an API key issue. Check your .env file.")
    
    if 'chatbot' not in st.session_state and 'vector_store' in st.session_state:
        retriever = st.session_state['vector_store'].as_retriever(search_kwargs={"k": 4})
        st.session_state['chatbot'] = PersonalChatbotAgent(retriever)
    
    # Main chat interface
    if 'chatbot' in st.session_state:
        # Display chat messages
        for message in st.session_state['messages']:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources if available
                if message["role"] == "assistant" and "sources" in message and message["sources"]:
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.write(f"**{i}. {source['filename']}** ({source['type']})")
                            st.text(source['content_preview'])
                            st.divider()
        
        # Handle sample question selection
        if 'current_question' in st.session_state:
            question = st.session_state['current_question']
            del st.session_state['current_question']
            
            # Add user message
            st.session_state['messages'].append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
            
            # Get and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state['chatbot'].ask(question)
                
                st.markdown(response['answer'])
                
                # Show sources
                if response['sources']:
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(response['sources'], 1):
                            st.write(f"**{i}. {source['filename']}** ({source['type']})")
                            st.text(source['content_preview'])
                            st.divider()
            
            # Add assistant message
            st.session_state['messages'].append({
                "role": "assistant", 
                "content": response['answer'],
                "sources": response['sources']
            })
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about Anees..."):
            # Add user message
            st.session_state['messages'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state['chatbot'].ask(prompt)
                
                st.markdown(response['answer'])
                
                # Show sources
                if response['sources']:
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(response['sources'], 1):
                            st.write(f"**{i}. {source['filename']}** ({source['type']})")
                            st.text(source['content_preview'])
                            st.divider()
            
            # Add assistant message
            st.session_state['messages'].append({
                "role": "assistant", 
                "content": response['answer'],
                "sources": response['sources']
            })
        
        # Clear conversation button
        if st.session_state['messages'] and st.button("🗑️ Clear Conversation"):
            st.session_state['messages'] = []
            if 'chatbot' in st.session_state:
                st.session_state['chatbot'].clear_memory()
            st.rerun()
    
    else:
        # No documents loaded
        st.info("👋 Welcome! To get started:")
        st.markdown("""
        1. **Add your documents** to the `data/` folder:
           - CV/Resume (PDF, DOCX, TXT)
           - Project descriptions (Markdown, TXT)
           - Code snippets (Python, JavaScript, etc.)
           - Blog posts or articles
           - Personal notes
        
        2. **Click 'Refresh Documents'** in the sidebar
        
        3. **Start chatting** with your personal AI assistant!
        """)
        
        # Create data folder if it doesn't exist
        if not os.path.exists(config.DATA_FOLDER):
            if st.button("📁 Create Data Folder"):
                os.makedirs(config.DATA_FOLDER, exist_ok=True)
                st.success(f"Created {config.DATA_FOLDER} folder! Now add your documents there.")
                st.rerun()

if __name__ == "__main__":
    main()
