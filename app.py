import streamlit as st
import os
from pathlib import Path

# Suppress warnings for cleaner output
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
    page_title="Anees's Personal AI Assistant (OpenAI)",
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
    if "personality_mode" not in st.session_state:
        st.session_state.personality_mode = config.DEFAULT_PERSONALITY_MODE
    if "vector_store_ready" not in st.session_state:
        st.session_state.vector_store_ready = False
    if "chatbot_agent" not in st.session_state:
        try:
            st.session_state.chatbot_agent = PersonalChatbotAgent(personality_mode=config.DEFAULT_PERSONALITY_MODE)
            # Try to automatically load documents from data folder on startup
            load_documents_from_data_folder()
        except ValueError as e:
            st.error(f"❌ Configuration Error: {str(e)}")
            if "Streamlit Cloud" in str(e) or "secrets" in str(e):
                st.info("💡 **For Streamlit Cloud deployment:** Add your `OPENAI_API_KEY` in the app's secrets settings")
            else:
                st.info("💡 **For local development:** Set `OPENAI_API_KEY` in your `.env` file or environment variables")
            st.session_state.chatbot_agent = None

def check_openai_status():
    """Check if OpenAI API is available and display status"""
    try:
        # Check if we have a valid chatbot agent
        if not hasattr(st.session_state, 'chatbot_agent') or st.session_state.chatbot_agent is None:
            st.error("❌ OpenAI API not configured")
            return False
            
        agent = st.session_state.chatbot_agent
        if agent.is_openai_available():
            st.success(f"✅ OpenAI API is available with model: {config.OPENAI_MODEL}")
            return True
        else:
            st.error("❌ OpenAI API is not available. Please check your API key.")
            return False
    except ValueError as e:
        st.error(f"❌ {str(e)}")
        st.info("💡 Please configure your OPENAI_API_KEY in Streamlit Cloud secrets or environment variables")
        return False
    except Exception as e:
        st.error(f"❌ Error connecting to OpenAI API: {str(e)}")
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
                vector_store = st.session_state.doc_processor.load_existing_vector_store()
                
                if vector_store:
                    # Check if vector store has content by trying to get the index size
                    try:
                        # FAISS vector stores don't have a direct count method, so we check if it exists
                        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
                        # Update existing chatbot agent with new retriever
                        if hasattr(st.session_state, "chatbot_agent") and st.session_state.chatbot_agent:
                            st.session_state.chatbot_agent.update_retriever(retriever)
                        else:
                            # Get personality mode safely
                            personality_mode = getattr(st.session_state, 'personality_mode', config.DEFAULT_PERSONALITY_MODE)
                            st.session_state.chatbot_agent = PersonalChatbotAgent(
                                vector_store_retriever=retriever, 
                                personality_mode=personality_mode
                            )
                        st.session_state.vector_store_ready = True
                        st.success(f"✅ Loaded existing FAISS vector store")
                        return True
                    except Exception as e:
                        st.info(f"Vector store exists but may be empty, processing documents... ({str(e)})")
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
                # Update existing chatbot agent with new retriever
                if hasattr(st.session_state, "chatbot_agent") and st.session_state.chatbot_agent:
                    st.session_state.chatbot_agent.update_retriever(retriever)
                else:
                    # Get personality mode safely
                    personality_mode = getattr(st.session_state, 'personality_mode', config.DEFAULT_PERSONALITY_MODE)
                    st.session_state.chatbot_agent = PersonalChatbotAgent(
                        vector_store_retriever=retriever, 
                        personality_mode=personality_mode
                    )
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
    # Initialize session state first
    initialize_session_state()
    
    st.title("🤖 Anees's Personal AI Assistant")
    
    # Display current mode in subtitle (with fallback)
    current_mode_key = getattr(st.session_state, 'personality_mode', config.DEFAULT_PERSONALITY_MODE)
    current_mode = config.PERSONALITY_MODES[current_mode_key]
    st.markdown(f"**Powered by OpenAI {config.OPENAI_MODEL} • Mode: {current_mode['name']}**")
    
    # Sidebar
    with st.sidebar:
        st.header("� Document Management")
        
        # Check Ollama status
        openai_available = check_openai_status()
        
        # Data folder info
        data_folder_exists = os.path.exists(config.DATA_FOLDER)
        if data_folder_exists:
            file_count = sum([len(files) for r, d, files in os.walk(config.DATA_FOLDER)])
            st.info(f"📊 Data folder: {file_count} files found")
        else:
            st.warning(f"📁 Data folder not found: {config.DATA_FOLDER}")
        
        # Refresh documents button
        if st.button("🔄 Refresh Documents", help="Reprocess documents from data folder") and openai_available:
            success = load_documents_from_data_folder()
            if success:
                st.rerun()
        
        # Personality Mode Selector
        st.subheader("🎭 Personality Mode")
        mode_options = {}
        for key, value in config.PERSONALITY_MODES.items():
            mode_options[value["name"]] = key
        
        current_mode_key = getattr(st.session_state, 'personality_mode', config.DEFAULT_PERSONALITY_MODE)
        current_mode_info = config.PERSONALITY_MODES[current_mode_key]
        
        selected_mode_name = st.selectbox(
            "Choose response style:",
            options=list(mode_options.keys()),
            index=list(mode_options.keys()).index(current_mode_info["name"]),
            help="Different modes change how Anees responds to your questions"
        )
        
        selected_mode_key = mode_options[selected_mode_name]
        
        # Show mode description
        st.info(f"📝 {config.PERSONALITY_MODES[selected_mode_key]['description']}")
        
        # Update personality mode if changed
        if selected_mode_key != current_mode_key:
            st.session_state.personality_mode = selected_mode_key
            if hasattr(st.session_state, "chatbot_agent") and st.session_state.chatbot_agent:
                success = st.session_state.chatbot_agent.set_personality_mode(selected_mode_key)
                if success:
                    st.success(f"✨ Switched to {selected_mode_name}")
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
        
        # Current mode display
        current_mode_key = getattr(st.session_state, 'personality_mode', config.DEFAULT_PERSONALITY_MODE)
        current_mode = config.PERSONALITY_MODES[current_mode_key]
        st.info(f"🎭 Current mode: **{current_mode['name']}**")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            if hasattr(st.session_state, "chatbot_agent"):
                st.session_state.chatbot_agent.clear_memory()
            st.rerun()
        
        # Model info
        st.subheader("🔧 Model Info")
        st.info(f"**Model**: {config.OPENAI_MODEL}")
        st.info("**Cost**: Pay per usage")
        st.info("**Privacy**: OpenAI API")
    
    # Main chat interface
    if not openai_available:
        st.warning("⚠️ OpenAI API is not available. Please check your API key.")
        st.info("Set your OPENAI_API_KEY environment variable or add it to a .env file")
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
                response = st.session_state.chatbot_agent.ask(prompt)
                answer = response["answer"]
                
                # Add context about document availability
                if not st.session_state.vector_store_ready and "source_documents" not in response:
                    answer += "\n\n*Note: I'm responding based on my general knowledge. Add documents to the data folder and refresh for personalized answers about Anees.*"
                
                st.markdown(answer)
                
                # Show source documents if available
                if st.session_state.vector_store_ready and "source_documents" in response and response["source_documents"]:
                    source_docs = response["source_documents"]
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
        current_mode_key = getattr(st.session_state, 'personality_mode', config.DEFAULT_PERSONALITY_MODE)
        current_mode = config.PERSONALITY_MODES[current_mode_key]
        st.subheader(f"💡 Sample Questions ({current_mode['name']})")
        
        # Mode-specific sample questions
        mode_questions = {
            "interview": [
                "What is your educational background?",
                "What are your key technical skills?",
                "What is your most significant project?",
                "What programming languages do you know?",
                "Tell me about your work experience"
            ],
            "storytelling": [
                "Tell me the story of your career journey",
                "What challenges have you overcome in your projects?",
                "How did you discover your passion for programming?",
                "What's the most interesting project you've worked on and why?",
                "What lessons have you learned throughout your career?"
            ],
            "fast_facts": [
                "Quick overview of your skills",
                "Your education and certifications",
                "Key projects - bullet points",
                "Programming languages and tech stack",
                "Work experience summary"
            ],
            "humble_brag": [
                "What are you most proud of in your career?",
                "What makes you stand out as a developer?",
                "What's your greatest technical achievement?",
                "Tell me about your most successful projects",
                "What unique value do you bring to teams?"
            ],
            "mentor": [
                "What advice would you give to new developers?",
                "What have you learned from your career challenges?",
                "How do you approach learning new technologies?",
                "What would you tell someone starting their career?",
                "What insights can you share from your experience?"
            ],
            "technical": [
                "Explain your most complex technical project",
                "What architectures have you worked with?",
                "Detail your development methodology",
                "What technical problems have you solved?",
                "Describe your technology stack expertise"
            ]
        }
        
        sample_questions = mode_questions.get(current_mode_key, [
            "What is Anees's educational background?",
            "What programming languages does Anees know?",
            "Tell me about Anees's work experience",
            "What projects has Anees worked on?",
            "What are Anees's technical skills?",
            "What is Anees's contact information?"
        ])
    
    cols = st.columns(min(3, len(sample_questions)))  # Max 3 columns
    for i, question in enumerate(sample_questions):
        col_idx = i % len(cols)
        if cols[col_idx].button(question, key=f"sample_{i}"):
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot_agent.ask(question)
                    answer = response["answer"]
                    
                    # Add context about document availability
                    if not st.session_state.vector_store_ready and "source_documents" not in response:
                        answer += "\n\n*Note: I'm responding based on my general knowledge. Add documents to the data folder and refresh for personalized answers about Anees.*"
                    
                    st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

if __name__ == "__main__":
    main()
